import csv
from shared_python.Args import Args
from shared_python.Sql import Sql
from html.parser import HTMLParser

from shared_python.Tags import Tags


def write_csv(filename, columns):
  html_parser = HTMLParser()
  with open(filename, 'wb') as fp:
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
  args_obj = Args()
  args = args_obj.args_for_03()
  log = args_obj.logger_with_filename()
  sql = Sql(args, log)
  tags = Tags(args, sql.db, log)

  log.info('Exporting tags from {0} to {1}'.format(args.temp_db_database, args.output_folder))
  cols = tags.tag_export_map
  results = tags.distinct_tags()
  write_csv('{0}/{1} - tags.csv'.format(args.output_folder, args.archive_name),
            [cols['id'], cols['original_tag'], cols['original_table'], cols['original_parent'],
             cols['ao3_tag_fandom'], cols['ao3_tag'], cols['ao3_tag_type'], cols['ao3_tag_category'],
             cols['original_description'], "TW Notes"])

  log.debug('Exporting authors with stories from {0} to {1}'.format(args.temp_db_database, args.output_folder))

  author_table = '{0}.authors'.format(args.temp_db_database)
  stories_table = '{0}.stories'.format(args.temp_db_database)
  item_authors_table = '{0}.item_authors'.format(args.temp_db_database)
  author_name = 'name'
  story_id = 'id'
  story_author_col = 'author_id'
  story_coauthor_col = 'coauthor_id'
  author_id = 'id'
  ia_author_col = 'author_id'
  ia_item_col = 'item_id'
    
  results = sql.execute("""
    SELECT s.{0} as "Story ID", s.title as "Title", s.summary as "Summary", a.{1} as "Creator", a.email as "Creator Email",
    "" as "New Email address", "" as "AO3 Account? (& does email match?)", "" as "Searched/Found", "" as "Work on AO3?",
    "" as "Import status", "" as "importer/inviter", "" as "import/invite date", "" as "AO3 link", "" as "Notes (if any)"
    FROM {2} ia join {3} a on ia.{4} = a.{5} join {6} s on ia.{7} = s.{8} where ia.item_type = "story";
    """.format(story_id, author_name, item_authors_table, author_table, ia_author_col, author_id, stories_table, ia_item_col, story_id))
  write_csv('{0}/{1} - authors with stories.csv'.format(args.output_folder, args.archive_name),
            ["Story ID", "Title", "Summary", "Creator", "Creator Email", "New Email address",
             "AO3 Account? (& does email match?)", "Searched/Found", "Work on AO3?", "Import status",
             "importer/inviter", "import/invite date", "AO3 link", "Notes (if any)"])



  log.debug('Exporting authors with bookmarks from {0} to {1}'.format(args.temp_db_database, args.output_folder))
  author_table = '{0}.authors'.format(args.temp_db_database)
  bookmarks_table = '{0}.story_links'.format(args.temp_db_database)
  item_authors_table = '{0}.item_authors'.format(args.temp_db_database)
  author_name = 'name'
  bookmark_id = 'id'
  bookmark_author_col = 'author_id'
  bookmark_coauthor_col = 'coauthor_id'
  author_id = 'id'
  ia_author_col = 'author_id'
  ia_item_col = 'item_id'

  results = sql.execute("""
      SELECT s.{0} as "Bookmark ID", s.title as "Title", s.summary as "Summary", a.{1} as "Creator", a.email as "Creator Email",
      s.url as "URL",
      "" as "New Email address", "" as "AO3 Account? (& does email match?)", "" as "Searched/Found", "" as "Work on AO3?",
      "" as "Import status", "" as "importer/inviter", "" as "import/invite date", "" as "AO3 link", "" as "Notes (if any)"
      FROM {2} ia join {3} a on ia.{4} = a.{5} join {6} s on ia.{7} = s.{8} where ia.item_type = "story_link";
    """.format(bookmark_id, author_name, item_authors_table, author_table, ia_author_col, author_id,  bookmarks_table, ia_item_col, bookmark_id))
  write_csv('{0}/{1} - authors with bookmarks.csv'.format(args.output_folder, args.archive_name),
              ["Bookmark ID", "Title", "Summary", "Creator", "Creator Email", "URL", "New Email address",
               "AO3 Account? (& does email match?)", "Searched/Found", "Work on AO3?", "Import status",
               "importer/inviter", "import/invite date", "AO3 link", "Notes (if any)"])
