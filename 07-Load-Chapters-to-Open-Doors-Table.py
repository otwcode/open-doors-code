# encoding: utf-8
import csv
import os

from automated_archive import aa
from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql


# Given an existing final chapter table, this will use the URL field and chapter location to load the chapter contents
def __current_table(table_name, db):
  query = "SELECT * FROM `{0}`.`{1}`".format(args.output_database, table_name)
  dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
  dict_cursor.execute(query)
  return dict_cursor.fetchall()


if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)
  chaps = Chapters(args, sql.db)

  table_names = {
    'authors': '{0}_authors'.format(args.db_table_prefix),
    'stories': '{0}_stories'.format(args.db_table_prefix),
    'chapters': '{0}_chapters'.format(args.db_table_prefix),
    'bookmarks': '{0}_bookmarks'.format(args.db_table_prefix)
  }

  print "Loading chapters from {0}...".format(args.chapters_path)

  # Current table contents
#  chapters = __current_table(table_names['chapters'], sql.db)

  chaps.populate_chapters()

  print('\n')
