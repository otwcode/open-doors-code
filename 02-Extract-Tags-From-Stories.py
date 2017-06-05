import re

from shared_python import Args
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  """
  This script creates a table called tags in the temporary database and denormalises all the tags for each story.
  This table is the basis for the Tag Wrangling sheet and is used to map the tags back to the story when the final
  tables are created.
  """
  args = Args.args_for_02()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  print('--- Processing tags from stories table in {0}'.format(args.temp_db_database))
  tags.create_tags_table()

# eg: python 01-Load-into-Mysql.py -dh localhost -du root -dt dsa -dd temp_python -a AA -f /Users/emma/OneDrive/DSA/ARCHIVE_DB.pl -o .
  tag_col_list = {}
  stories_id_name = ""
  stories_table_name = ""

  # AUTOMATED ARCHIVE
  if args.archive_type == 'AA':

    table_name = raw_input('Story table name (default: "{0}_stories"): '.format(args.db_table_prefix))
    if table_name is None or table_name == '':
      table_name = '{0}_stories'.format(args.db_table_prefix)
    tag_columns = raw_input('Column names containing tags \n   (delimited by commas - default: "rating, tags, warnings, characters, fandoms, relationships"): ')
    if tag_columns is None or tag_columns == '':
      tag_columns = "rating, tags, warnings, characters, fandoms, relationships"
    # fancy footwork to ensure compatibility with eFiction
    tag_col_list = re.split(r", ?", tag_columns)
    tag_columns_dict = dict(zip(tag_col_list, tag_col_list))
    tags.populate_tag_table(args.temp_db_database, "id", table_name, tag_columns_dict)

  # EFICTION
  elif args.archive_type == 'EF':
    from eFiction import efiction
    tag_columns = raw_input('Column names containing tags \n   (delimited by commas - default: "catid, classes, charid, rid, gid, wid"): ')
    if tag_columns is None or tag_columns == '':
      tag_columns = "catid, classes, charid, rid, gid, wid"

    for col in re.split(r", ?", tag_columns):
      if sql.col_exists(col, "fanfiction_stories", args.temp_db_database):
        tag_col_list[col] = efiction.column_schema(col)

    tags.populate_tag_table(args.temp_db_database, "sid", "fanfiction_stories", tag_col_list)

    has_ids_in_tags = raw_input('Do all the tag fields contain ids? (y, n) ')
    for col in tag_col_list.keys():
      print "\nProcessing {0}".format(col)
      table = efiction.column_schema(col)
      tags.hydrate_tags_table(col, table, has_ids_in_tags == 'y')
