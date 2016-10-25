# encoding: utf-8
import csv

from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  final = FinalTables(args, sql.db)
  chaps = Chapters(args, sql.db)

  filter = ''
  coauthors = {}
  if args.archive_type == 'EF':
    table_names = efiction.table_names()
    coauthors_dict = sql.execute_dict("SELECT * FROM fanfiction_coauthors")
    for coauthor in coauthors_dict:
      coauthors[coauthor['sid']] = coauthor['uid']
    filter = 'WHERE sid NOT IN '
  else:
    table_names = {
      'authors': 'authors',
      'stories': 'stories',
      'chapters': 'chapters'
    }
    filter = 'WHERE id NOT IN '

  sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                           database=args.output_database,
                           prefix=args.db_table_prefix + '_')

  story_exclusion_filter = ''
  # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
  with open(args.story_ids_to_remove, "rt") as f:
    for line in f:
      story_exclusion_filter = filter + '(' + line + ')'

  # Export tables
  authors = final.original_table(table_names['authors'])
  stories_without_tags = final.original_table(table_names['stories'], story_exclusion_filter)
  chapters = final.original_table(table_names['chapters'], story_exclusion_filter)
  # there are usually no bookmarks




  if args.archive_type == 'AA':
    print 'Not implemented yet'

  elif args.archive_type == 'EF':
    final_authors = [efiction.author_to_final(author) for author in authors]
    final.insert_into_final(args.db_table_prefix + '_authors', final_authors)

    final_stories = []
    for story in stories_without_tags:
      if coauthors is not None and coauthors.has_key(story['sid']):
        story['coauthors'] = coauthors[story['sid']]
      else:
        story['coauthors'] = None
      final_stories.append(efiction.story_to_final_without_tags(story))

    final.insert_into_final(args.db_table_prefix + '_stories', final_stories)

    final_chapters = [efiction.chapter_to_final(chapter) for chapter in chapters]
    final.insert_into_final(args.db_table_prefix + '_chapters', final_chapters)

    # Run chapter script
    chaps.populate_chapters()

    # TODO: bookmarks



