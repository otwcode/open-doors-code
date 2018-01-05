# encoding: utf-8
import os

from automated_archive import aa
from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags


def _clean_email(author):
  email = author['email']
  if author['email'] is None or author['email'] == '':
    email = u'{0}{1}Archive@ao3.org'.format(author['name'], args.archive_name)\
      .replace(' ', '').replace("'", "")
  if author['email'].startswith('mailto:'):
    email = author['email'].replace('mailto:', '')
  return email


if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  final = FinalTables(args, sql.db)
  chaps = Chapters(args, sql.db)

  filter = ''
  coauthors = {}

  print "Creating destination tables in {0}".format(args.output_database)

  if args.archive_type == 'EF':
    table_names = efiction.table_names()
    has_coauthor_table = raw_input("\nDoes this archive have a coauthors table? Y/N\n")
    has_coauthors = True if str.lower(has_coauthor_table) == 'y' else False
    if has_coauthors:
      coauthors_dict = sql.execute_dict("SELECT * FROM fanfiction_coauthors")
      for coauthor in coauthors_dict:
        coauthors[coauthor['sid']] = coauthor['uid']
    filter = 'WHERE sid NOT IN '
  else:
    table_names = {
      'authors': '{0}_authors'.format(args.db_table_prefix),
      'stories': '{0}_stories'.format(args.db_table_prefix),
      'chapters': '{0}_chapters'.format(args.db_table_prefix),
      'bookmarks': '{0}_bookmarks'.format(args.db_table_prefix)
    }
    filter = 'WHERE id NOT IN '

  sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                           database=args.output_database,
                           prefix=args.db_table_prefix + '_')

  story_exclusion_filter = ''
  # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
  if os.path.exists(args.story_ids_to_remove):
    with open(args.story_ids_to_remove, "rt") as f:
      print "Removing {0} Do Not Import stories...".format(sum(line.count(",") for line in f))
      f.seek(0)
      for line in f:
        story_exclusion_filter = filter + '(' + line + ')'


  # Export tables
  stories_without_tags = final.original_table(table_names['stories'], story_exclusion_filter)
  print "Stories without tags: {0}".format(len(stories_without_tags))
  chapters = final.original_table(table_names['chapters'], '')
  bookmarks_without_tags = final.original_table(table_names['bookmarks'], story_exclusion_filter)


  # ----------------------
  # AA and custom archives
  # ----------------------
  if args.archive_type == 'AA':
    # STORIES
    print "Copying stories to final table {0}.{1}_stories...".format(args.output_database, args.db_table_prefix)
    final_stories = []
    for story in stories_without_tags:
      # Add additional story processing here
      final_stories.append(aa.story_to_final_without_tags(story))
    final.insert_into_final(args.db_table_prefix + '_stories', final_stories)

    # BOOKMARKS
    if bookmarks_without_tags is not None:
      print "Copying bookmarks to final table {0}.{1}_bookmarks...".format(args.output_database, args.db_table_prefix)
      final_bookmarks = []
      for bookmark in bookmarks_without_tags:
        # Add additional bookmark processing here
        final_bookmarks.append(aa.story_to_final_without_tags(bookmark, False))
      if final_bookmarks: final.insert_into_final(args.db_table_prefix + '_bookmarks', final_bookmarks)

    # AUTHORS
    print "Copying authors to final table {0}.{1}_authors, cleaning emails and removing authors with no works...".format(args.output_database, args.db_table_prefix)
    final_authors = []
    authors = final.original_table(table_names['authors'])
    for final_author in authors:
      if any(story['authorid'] == final_author['id'] or story['coauthorid'] == final_author['id'] for story in final_stories):
        final_author['email'] = _clean_email(final_author)
      final_authors.append(final_author)
    final.insert_into_final(args.db_table_prefix + '_authors', final_authors)

    # CHAPTERS
    if chapters:
      print "Copying chapters table {0}.{1}_chapters from source chapters table...".format(args.output_database, args.db_table_prefix)
      truncate_and_insert = "truncate {0}.{1}; insert into {0}.{1} select * from {2}.{3};".format(
        args.output_database,
        table_names['chapters'],
        args.temp_db_database,
        table_names['chapters'])
      sql.execute(truncate_and_insert)
    else:
      print "Creating chapters table {0}.{1}_chapters from source stories table...".format(args.output_database, args.db_table_prefix)
      final_chapters = aa.dummy_chapters(final_stories)
      final.insert_into_final(args.db_table_prefix + '_chapters', final_chapters)


  # ----------------------
  # eFiction
  # ----------------------
  elif args.archive_type == 'EF':
    # STORIES
    print "Copying stories to final table {0}.{1}_stories...".format(args.output_database, args.db_table_prefix)
    final_stories = []
    for story in stories_without_tags:
      if coauthors is not None and coauthors.has_key(story['sid']):
        story['coauthors'] = coauthors[story['sid']]
      else:
        story['coauthors'] = None
      final_stories.append(efiction.story_to_final_without_tags(story))

    final.insert_into_final(args.db_table_prefix + '_stories', final_stories)

    # BOOKMARKS
    if bookmarks_without_tags is not None:
      print "Copying bookmarks to final table {0}.{1}_bookmarks...".format(args.output_database, args.db_table_prefix)
      final_bookmarks = []
      for bookmark in bookmarks_without_tags:
        # Add additional bookmark processing here
        final_bookmarks.append(aa.story_to_final_without_tags(bookmark))
      if final_bookmarks: final.insert_into_final(args.db_table_prefix + '_bookmarks', final_bookmarks)

    # AUTHORS
    print "Copying authors from original eFiction source, cleaning emails and removing authors with no works..."
    final_authors = []
    authors = final.original_table(table_names['authors'])
    for author in authors:
      final_author = efiction.author_to_final(author)
      if any(story['authorid'] == final_author['id'] or story['coauthorid'] == final_author['id'] for story in final_stories):
        final_author['email'] = _clean_email(final_author)
      final_authors.append(final_author)
    final.insert_into_final(args.db_table_prefix + '_authors', final_authors)

    # CHAPTERS
    print "Copying chapters from original eFiction source..."
    final_chapters = [efiction.chapter_to_final(chapter) for chapter in chapters]
    final.insert_into_final(args.db_table_prefix + '_chapters', final_chapters)

  print('\n')
