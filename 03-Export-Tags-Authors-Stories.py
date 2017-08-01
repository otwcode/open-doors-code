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
  """
  This step exports the Tag Wrangling and Authors with stories CSV files which you then have to import into Google
  Spreadsheet and share with the rest of the Open Doors committee.
  """
  args = Args.args_for_03()
  sql = Sql(args)
  tags = Tags(args, sql.db)

  print('Exporting tags from {0} to {1}'.format(args.temp_db_database, args.output_folder))
  cols = tags.tag_export_map
  results = tags.distinct_tags()
  write_csv('{0}/{1} - tags.csv'.format(args.output_folder, args.archive_name),
            [cols['original_tagid'], cols['original_tag'], cols['original_table'], cols['original_parent'],
             cols['ao3_tag_fandom'], cols['ao3_tag'], cols['ao3_tag_type'], cols['ao3_tag_category'],
             cols['original_description'], "TW Notes"])

  print('Exporting authors with stories from {0} to {1}'.format(args.temp_db_database, args.output_folder))
  if args.archive_type == 'AA':
    author_table = '{0}.{1}_authors'.format(args.temp_db_database, args.db_table_prefix)
    stories_table = '{0}.{1}_stories'.format(args.temp_db_database, args.db_table_prefix)
    author_name = 'name'
    story_id = 'id'
    story_author_col = 'authorId'
    story_coauthor_col = 'coAuthorId'
    author_id = 'id'
  elif args.archive_type == 'EF':
    author_table = '{0}.fanfiction_authors'.format(args.temp_db_database)
    stories_table = '{0}.fanfiction_stories'.format(args.temp_db_database)
    author_name = 'penname'
    story_id = 'sid'
    story_author_col = 'uid'
    author_id = 'uid'

  results = sql.execute("""
    SELECT s.{0} as "Story ID", s.title as "Title", s.summary as "Summary", a.{1} as "Creator", a.email as "Creator Email",
    "" as "New Email address", "" as "AO3 Account? (& does email match?)", "" as "Searched/Found", "" as "Work on AO3?",
    "" as "Import status", "" as "importer/inviter", "" as "import/invite date", "" as "AO3 link", "" as "Notes (if any)"
    FROM {2} a join {3} s on s.{4} = a.{5};
  """.format(story_id, author_name, author_table, stories_table, story_author_col, author_id))
  write_csv('{0}/{1} - authors with stories.csv'.format(args.output_folder, args.archive_name),
            ["Story ID", "Title", "Summary", "Creator", "Creator Email", "New Email address",
             "AO3 Account? (& does email match?)", "Searched/Found", "Work on AO3?", "Import status",
             "importer/inviter", "import/invite date", "AO3 link", "Notes (if any)"])


  if args.archive_type == 'AA':
    print('Exporting authors with bookmarks from {0} to {1}'.format(args.temp_db_database, args.output_folder))
    author_table = '{0}.{1}_authors'.format(args.temp_db_database, args.db_table_prefix)
    bookmarks_table = '{0}.{1}_bookmarks'.format(args.temp_db_database, args.db_table_prefix)
    author_name = 'name'
    bookmark_id = 'id'
    bookmark_author_col = 'authorId'
    bookmark_coauthor_col = 'coAuthorId'
    author_id = 'id'

    results = sql.execute("""
      SELECT s.{0} as "Bookmark ID", s.title as "Title", s.summary as "Summary", a.{1} as "Creator", a.email as "Creator Email",
      s.url as "URL",
      "" as "New Email address", "" as "AO3 Account? (& does email match?)", "" as "Searched/Found", "" as "Work on AO3?",
      "" as "Import status", "" as "importer/inviter", "" as "import/invite date", "" as "AO3 link", "" as "Notes (if any)"
      FROM {2} a join {3} s on s.{4} = a.{5};
    """.format(bookmark_id, author_name, author_table, bookmarks_table, bookmark_author_col, author_id))
    write_csv('{0}/{1} - authors with bookmarks.csv'.format(args.output_folder, args.archive_name),
              ["Bookmark ID", "Title", "Summary", "Creator", "Creator Email", "URL", "New Email address",
               "AO3 Account? (& does email match?)", "Searched/Found", "Work on AO3?", "Import status",
               "importer/inviter", "import/invite date", "AO3 link", "Notes (if any)"])

  print('\n')
