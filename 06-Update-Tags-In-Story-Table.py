# encoding: utf-8
import csv

from eFiction import efiction
from shared_python import Args
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_05() # Not a typo!
  sql = Sql(args)
  tags = Tags(args, sql.db)
  final = FinalTables(args, sql.db)

  if args.archive_type == 'EF':
    table_names = efiction.table_names()
  else:
    table_names = {
      'authors': 'authors',
      'stories': 'stories',
      'chapters': 'chapters'
    }

  if args.archive_type == 'AA':
    print 'Not implemented yet'

  elif args.archive_type == 'EF':
    print "Getting all tags per story..."
    tags_by_story_id = tags.tags_by_story_id()
    for (story_id, tags) in tags_by_story_id.items():

      # group tags by type into comma-separated lists
      # generate and run SQL to populate story table
      from collections import defaultdict

      tags_by_type = defaultdict(list)  # key -> sum
      for tag in tags:
        tags_by_type[tag['ao3_tag_type']].append(tag)

      story_tags = {}
      for (tag_type, tag_type_tags) in tags_by_type.items():
        if tag_type is None:
          print "\nStory {2} has a None tag type\n {0} -> {1}".format(tag_type, tag_type_tags, id)
        else:
          tag_list = [d['ao3_tag'] for d in tag_type_tags if 'ao3_tag' in d and d['ao3_tag'] is not None]
          story_tags[tag_type] = ', '.join(tag_list)

      final.populate_story_tags(story_id, args.db_table_prefix + '_stories', story_tags)
