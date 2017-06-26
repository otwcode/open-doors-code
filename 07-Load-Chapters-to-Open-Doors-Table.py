# encoding: utf-8
import csv
import os

from automated_archive import aa
from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)
  final = FinalTables(args, sql.db)
  chaps = Chapters(args, sql.db)

  table_names = {
    'authors': '{0}_authors'.format(args.db_table_prefix),
    'stories': '{0}_stories'.format(args.db_table_prefix),
    'chapters': '{0}_chapters'.format(args.db_table_prefix),
    'bookmarks': '{0}_bookmarks'.format(args.db_table_prefix)
  }

  # Export tables
  final_stories = final.original_table(table_names['stories'], story_exclusion_filter)
  chapters = final.original_table(table_names['chapters'], '')

  if args.archive_type == 'AA':
    # CHAPTERS
    print "Chapters..."
    final_chapters = aa.dummy_chapters(final_stories)
    final.insert_into_final(args.db_table_prefix + '_chapters', final_chapters)

    # Run chapter script
    chaps.populate_chapters()

  elif args.archive_type == 'EF':

    # CHAPTERS
    print "Chapters..."
    final_chapters = [efiction.chapter_to_final(chapter) for chapter in chapters]
    final.insert_into_final(args.db_table_prefix + '_chapters', final_chapters)

    # Run chapter script
    chaps.populate_chapters()

  print('\n')
