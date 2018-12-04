# encoding: utf-8
import os

from automated_archive import aa
from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Logging import log
from shared_python.Sql import Sql
from shared_python.Tags import Tags


def _clean_email(author):
  email = author['email']
  if email is None or email == '':
    email = u'{0}{1}Archive@ao3.org'.format(author['name'], args.archive_name)\
      .replace(' ', '').replace("'", "")
  if email.startswith('mailto:'):
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

  log.info("Creating destination tables in {0}".format(args.output_database))

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
      'authors': 'authors',
      'stories': 'stories',
      'chapters': 'chapters',
      'story_links': 'story_links'
    }
    filter = 'WHERE id NOT IN '

  sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                           database=args.output_database)


  story_exclusion_filter = ''
  # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
  if os.path.exists(args.story_ids_to_remove):
    with open(args.story_ids_to_remove, "rt") as f:
      log.info("Removing {0} Do Not Import stories...".format(sum(line.count(",") for line in f) + 1))
      f.seek(0)
      for line in f:
        story_exclusion_filter = filter + '(' + line + ')'

  bookmark_exclusion_filter = ''
  # Filter out DNI stories - bookmark_ids_to_remove must be comma-separated list of DNI ids
  if args.bookmark_ids_to_remove and os.path.exists(args.bookmark_ids_to_remove):
    with open(args.bookmark_ids_to_remove, "rt") as f:
      log.info("Removing {0} Do Not Import bookmarks...".format(sum(line.count(",") for line in f) + 1))
      f.seek(0)
      for line in f:
        bookmark_exclusion_filter = filter + '(' + line + ')'


  # Export tables
  stories_without_tags = final.original_table(table_names['stories'], story_exclusion_filter)
  log.info("Stories without tags after removing DNI: {0}".format(len(stories_without_tags)))
  bookmarks_without_tags = final.original_table(table_names['bookmarks'], bookmark_exclusion_filter)
  if bookmarks_without_tags:
    log.info("Bookmarks without tags after removing DNI: {0}".format(len(bookmarks_without_tags)))
  else:
    log.info("No bookmarks to remove")

  chapters = final.original_table(table_names['chapters'], '')


  # ----------------------
  # AA and custom archives
  # ----------------------
  if args.archive_type == 'AA':
    # STORIES
    log.info("Copying stories to final table {0}.stories...".format(args.output_database))
    final_stories = []
    for story in stories_without_tags:
      # Add additional story processing here
      final_stories.append(aa.story_to_final_without_tags(story))
    final.insert_into_final('stories', final_stories)

    # BOOKMARKS
    if bookmarks_without_tags is not None:
      log.info("Copying bookmarks to final table {0}.bookmarks...".format(args.output_database))
      final_bookmarks = []
      for bookmark in bookmarks_without_tags:
        # Add additional bookmark processing here
        final_bookmarks.append(aa.story_to_final_without_tags(bookmark, False))
      if final_bookmarks: final.insert_into_final('bookmarks', final_bookmarks)

    # AUTHORS
    log.info("Copying authors to final table {0}.authors, cleaning emails and removing authors with no works...".format(args.output_database))
    final_authors = []
    authors = final.original_table(table_names['authors'])
    for final_author in authors:
      if any(story['author_id'] == final_author['id'] or story['coauthor_id'] == final_author['id'] for story in final_stories)\
          or any(bookmark['author_id'] == final_author['id'] for bookmark in final_bookmarks):
        final_author['email'] = _clean_email(final_author)
        final_authors.append(final_author)
    final.insert_into_final('authors', final_authors)

    # CHAPTERS
    if chapters:
      dest_chapter_table = "{0}.{1}".format(args.output_database, table_names['chapters'])
      log.info("Copying chapters table {0} from source chapters table...".format(dest_chapter_table))
      sql.execute("drop table if exists {0}".format(dest_chapter_table))

      truncate_and_insert = "create table {0} select * from {1}.{2}".format(
        dest_chapter_table,
        args.temp_db_database,
        table_names['chapters'])
      sql.execute(truncate_and_insert)
    else:
      log.info("Creating chapters table {0}.chapters from source stories table...".format(args.output_database))
      final_chapters = aa.dummy_chapters(final_stories)
      final.insert_into_final('chapters', final_chapters)


  # ----------------------
  # eFiction
  # ----------------------
  elif args.archive_type == 'EF':
    # STORIES
    log.info("Copying stories to final table {0}.stories...".format(args.output_database))
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
      log.info("Copying bookmarks to final table {0}.bookmarks...".format(args.output_database))
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
      if any(story['author_id'] == final_author['id'] or story['coauthor_id'] == final_author['id'] for story in final_stories):
        final_author['email'] = _clean_email(final_author)
      final_authors.append(final_author)
    final.insert_into_final('authors', final_authors)

    # CHAPTERS
    log.info("Copying chapters from original eFiction source...")
    final_chapters = [efiction.chapter_to_final(chapter) for chapter in chapters]
    final.insert_into_final('chapters', final_chapters)
