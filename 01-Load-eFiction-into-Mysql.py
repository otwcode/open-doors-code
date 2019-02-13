import re

from automated_archive import aa
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags
from eFiction import efiction


if __name__ == "__main__":
  args = Args.args_for_01()
  log = args.logger_with_filename()
  sql = Sql(args)

  original_database = "{}_efiction".format(args.temp_db_database)
  log.info('Loading eFiction file "{0}" into database "{1}"'.format(args.db_input_file, original_database))
  sql.run_script_from_file(args.db_input_file,
                           database = args.temp_db_database,
                           initial_load = True)

  # Extract tags
  args = Args.args_for_02()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  log.info('Processing tags from stories and bookmarks table in {0}'.format(original_database))
  tags.create_tags_table()

  tag_col_list = {}
  stories_id_name = ""
  stories_table_name = ""
  tag_columns = raw_input('Column names containing tags \n   (delimited by commas - default: "catid, classes, charid, rid, gid, wid"): ')
  if tag_columns is None or tag_columns == '':
    tag_columns = "catid, classes, charid, rid, gid, wid"

  for col in re.split(r", ?", tag_columns):
    if sql.col_exists(col, "fanfiction_stories", original_database):
      tag_col_list[col] = efiction.column_schema(col)

  tags.populate_tag_table(original_database, "sid", "fanfiction_stories", tag_col_list, '')

  has_ids_in_tags = raw_input('Do all the tag fields contain ids? (y, n) ')
  for col in tag_col_list.keys():
    log.debug("Processing {0}".format(col))
    table = efiction.column_schema(col)
    tags.hydrate_tags_table(col, table, has_ids_in_tags == 'y')

  # Create intermediate database
  coauthors = {}
  table_names = efiction.table_names()
  has_coauthor_table = raw_input("\nDoes this archive have a coauthors table? Y/N\n")
  has_coauthors = True if str.lower(has_coauthor_table) == 'y' else False
  if has_coauthors:
    coauthors_dict = sql.execute_dict("SELECT * FROM fanfiction_coauthors")
    for coauthor in coauthors_dict:
      coauthors[coauthor['sid']] = coauthor['uid']
  filter = 'WHERE sid NOT IN '

  sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                           database=args.temp_db_database)

  # Export tables
  args = Args.args_for_05()
  final = FinalTables(args, sql.db)
  chaps = Chapters(args, sql.db)
  stories_without_tags = final.original_table(table_names['stories'])
  log.info("Stories without tags in original eFiction: {0}".format(len(stories_without_tags)))
  bookmarks_without_tags = final.original_table(table_names['bookmarks'])
  if bookmarks_without_tags:
    log.info("Bookmarks without tags in original eFiction: {0}".format(len(bookmarks_without_tags)))
  else:
    log.info("No bookmarks to remove")

  chapters = final.original_table(table_names['chapters'], '')

  # STORIES
  log.info("Copying stories to temporary table {0}.stories...".format(args.temp_db_database))
  final_stories = []
  for story in stories_without_tags:
    if coauthors is not None and coauthors.has_key(story['sid']):
      story['coauthors'] = coauthors[story['sid']]
    else:
      story['coauthors'] = None
    final_stories.append(efiction.story_to_final_without_tags(story))

  final.insert_into_final('stories', final_stories)

  # BOOKMARKS
  if bookmarks_without_tags is not None:
    log.info("Copying bookmarks to final table {0}.bookmarks...".format(args.temp_db_database))
    final_bookmarks = []
    for bookmark in bookmarks_without_tags:
      # Add additional bookmark processing here
      final_bookmarks.append(aa.story_to_final_without_tags(bookmark))
    if final_bookmarks: final.insert_into_final('bookmarks', final_bookmarks)

  # AUTHORS
  log.info("Copying authors from original eFiction source, cleaning emails and removing authors with no works...")
  final_authors = []
  authors = final.original_table(table_names['authors'])
  for author in authors:
    final_author = efiction.author_to_final(author)
    final_authors.append(final_author)
  final.insert_into_final('authors', final_authors)

  # CHAPTERS
  log.info("Copying chapters from original eFiction source...")
  final_chapters = [efiction.chapter_to_final(chapter) for chapter in chapters]
  final.insert_into_final('chapters', final_chapters)