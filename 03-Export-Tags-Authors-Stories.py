import csv
from shared_python import Args
from shared_python.Sql import Sql
from HTMLParser import HTMLParser

from shared_python.Tags import Tags


def write_csv(filename, columns):
  html_parser = HTMLParser()
  with open(filename, 'w') as fp:
    myFile = csv.writer(fp)
    myFile.writerow(columns)
    for row in results:
      r = []
      for s in row:
        r.append('' if s is None else html_parser.unescape(unicode(s)).encode('utf-8'))
      myFile.writerows([r])
    fp.close()


if __name__ == "__main__":
  args = Args.args_for_03()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  print('--- Exporting tags from {0}'.format(args.db_database))
  cols = tags.tag_export_map
  results = tags.distinct_tags()
  write_csv('{0} - tags.csv'.format(args.db_database),
            [cols['original_tagid'], cols['original_tag'], cols['original_table'], cols['original_parent'],
             cols['ao3_tag_fandom'], cols['ao3_tag'], cols['ao3_tag_type'], cols['ao3_tag_category'],
             cols['original_description'], "TW Notes"])

  print('--- Exporting authors with stories from {0}'.format(args.db_database))
  if args.archive_type == 'AA':
    author_table = '{0}.{1}_authors'.format(args.db_database, args.db_table_prefix)
    stories_table = '{0}.{1}_stories'.format(args.db_database, args.db_table_prefix)
    author_name = 'name'
    story_id = 'id'
    story_author_col = 'authorId'
    author_id = 'id'
  if args.archive_type == 'EF':
    author_table = '{0}.fanfiction_authors'.format(args.db_database)
    stories_table = '{0}.fanfiction_stories'.format(args.db_database)
    author_name = 'penname'
    story_id = 'sid'
    story_author_col = 'uid'
    author_id = 'uid'

  results = sql.execute("""
    SELECT s.{0} as "Story ID", s.title as "Title", s.summary as "Summary", a.{1} as "Creator", a.email as "Creator Email"
    FROM {2} a join {3} s on s.{4} = a.{5};
  """.format(story_id, author_name, author_table, stories_table, story_author_col, author_id))
  write_csv('{0} - authors with stories.csv'.format(args.db_database), ["Title", "Summary", "Creator", "Creator Email"])
