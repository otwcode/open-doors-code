# encoding: utf-8
import csv

from eFiction import efiction
from shared_python import Args
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags


def valid_tags(key, tag_type_list):
  return [d[key].strip() for d in tag_type_list
          if key in d
          and d[key] is not None
          and d[key] != '']


if __name__ == "__main__":
  args = Args.args_for_06()
  log = args.logger_with_filename()
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

  log.info("Getting all tags per story...")
  tags_by_story_id = tags.tags_by_story_id()
  for (story_id, tags) in tags_by_story_id.items():

    # group tags by type into comma-separated lists
    # generate and run SQL to populate story table
    from collections import defaultdict

    tags_by_type = defaultdict(list)
    for tag in tags:
      tags_by_type[tag['ao3_tag_type']].append(tag)

    story_tags = { 'categories': '', 'fandoms': '' }
    categories = []
    fandoms = [args.default_fandom]
    for (tag_type, tag_type_tags) in tags_by_type.items():
      if tag_type is None or tag_type == '':
        log.warn("\nStory {2} has a None tag type\n {0} -> {1}".format(tag_type, tag_type_tags, story_id))
      else:
        tag_list = [d['ao3_tag'] for d in tag_type_tags if 'ao3_tag' in d and d['ao3_tag'] is not None]
        categories += valid_tags('ao3_tag_category', tag_type_tags)
        if tag_type == 'fandoms':
          fandoms += tag_list
        # Don't add the related fandom for this tag
        # else:
        #   fandoms += valid_tags('ao3_tag_fandom', tag_type_tags)
        story_tags[tag_type] = ', '.join(set(tag_list))

    story_tags['categories'] = ', '.join(set(categories))
    story_tags['fandoms'] = ', '.join(set(fandoms))

    final.populate_story_tags(story_id, 'stories', story_tags)
    final.populate_story_tags(story_id, 'story_links', story_tags)
