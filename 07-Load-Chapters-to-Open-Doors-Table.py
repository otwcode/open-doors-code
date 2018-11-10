# encoding: utf-8
import csv
import os

from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.Sql import Sql

import logging
import sys
logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
log = logging.getLogger()

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


  log.info("Loading chapters from {0}...".format(args.chapters_path))
  chaps.populate_chapters()
