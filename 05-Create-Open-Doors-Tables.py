# encoding: utf-8
import csv

from eFiction import efiction
from shared_python import Args
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)
  tags = Tags(args)
  final = FinalTables(args, sql.db)

  if args.archive_type == 'EF':
    table_names = efiction.table_names()
  else:
    table_names = {
      'authors': 'authors',
      'stories': 'stories',
      'chapters': 'chapters'
    }

  sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                           database=args.output_database,
                           prefix=args.db_table_prefix + '_')

  # Export authors
  authors = final.original_table(table_names['authors'])
  stories_without_tags = final.original_table(table_names['stories'])
  chapters = final.original_table(table_names['chapters'])
  # there are usually no bookmarks

  if args.archive_type == 'AA':
    print 'Not implemented yet'

  elif args.archive_type == 'EF':
    final_authors = [efiction.author_to_final(author) for author in authors]
    final.insert_into_final(args.db_table_prefix + '_authors', final_authors)

    final_stories = []
    for story in stories_without_tags:
      final_stories.append(efiction.story_to_final_without_tags(story))
    final.insert_into_final(args.db_table_prefix + '_stories', final_stories)

# TODO chapters and bookmarks
