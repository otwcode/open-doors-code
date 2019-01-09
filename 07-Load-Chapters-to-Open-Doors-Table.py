# encoding: utf-8
import MySQLdb

from shared_python.Args import Args
from shared_python.Chapters import Chapters
from shared_python.Sql import Sql


# Given an existing final chapter table, this will use the URL field and chapter location to load the chapter contents
def __current_table(table_name, db):
  query = "SELECT * FROM `{0}`.`{1}`".format(args.output_database, table_name)
  dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
  dict_cursor.execute(query)
  return dict_cursor.fetchall()


if __name__ == "__main__":
  argsClass = Args()
  args = argsClass.args_for_05()
  log = argsClass.logger_with_filename()
  sql = Sql(args, log)
  chaps = Chapters(args, sql.db, log)


  log.info("Loading chapters from {0}...".format(args.chapters_path))
  chaps.populate_chapters()
