#!/usr/bin/env python3

from pymysql import cursors

from shared_python.Args import Args
from shared_python.Chapters import Chapters
from shared_python.Sql import Sql


# Given an existing final chapter table, this will use the URL field and chapter location to load the chapter contents
def __current_table(table_name, db):
    query = f"SELECT * FROM `{args.output_database}`.`{table_name}`"
    dict_cursor = db.cursor(cursors.DictCursor)
    dict_cursor.execute(query)
    return dict_cursor.fetchall()


if __name__ == "__main__":
    # TODO the eFiction process now loads chapters into MySQL before further processing in ODAP, all others should too
    args_obj = Args()
    args = args_obj.args_for_07()
    log = args_obj.logger_with_filename()
    sql = Sql(args, log)
    chaps = Chapters(args, sql, log)

    log.info(f"Loading chapters from {args.chapters_path}...")
    chaps.populate_chapters()
