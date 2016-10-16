import re

from shared_python import Args
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_02()
  sql = Sql(args)
  tags = Tags(args, sql.db)
  print('--- Processing tags from stories table in {0}'.format(args.db_database))
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
    tag_columns = raw_input('Column names containing tags \n   (delimited by commas - default: "tags, warnings, characters, fandoms, relationships"): ')
    if tag_columns is None or tag_columns == '':
      tag_columns = "tags, warnings, characters, fandoms, relationships"
    tags.populate_tag_table(args.db_database, "id", table_name, tag_columns)

  # EFICTION
  elif args.archive_type == 'EF':
    from eFiction import efiction
    tag_columns = raw_input('Column names containing tags \n   (delimited by commas - default: "catid, classes, charid, rid, gid, wid"): ')
    if tag_columns is None or tag_columns == '':
      tag_columns = "catid, classes, charid, rid, gid, wid"

    for col in re.split(r", ?", tag_columns):
      if sql.col_exists(col, "fanfiction_stories", args.db_database):
        tag_col_list[col] = efiction.column_schema(col)

    tags.populate_tag_table(args.db_database, "sid", "fanfiction_stories", tag_col_list)

    has_ids_in_tags = raw_input('Do all the tag fields contain ids? (y, n) ')
    for col in tag_col_list.keys():
      print "\nProcessing {0}".format(col)
      table = efiction.column_schema(col)
      tags.hydrate_tags_table(col, table, has_ids_in_tags == 'y')
