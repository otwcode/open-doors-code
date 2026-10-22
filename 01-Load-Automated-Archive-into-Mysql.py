#!/usr/bin/env python3

from automated_archive import aa
from shared_python.Args import Args
from shared_python.Sql import Sql

if __name__ == "__main__":
    args_obj = Args()
    args = args_obj.args_for_01()
    log = args_obj.logger_with_filename()
    sql = Sql(args, log)

    # eg: python 01-Load-Automated-Archive-into-Mysql.py -dh localhost -du root -dt dsa -dd temp_python -a AA -f /path/to/ARCHIVE_DB.pl -o .
    log.info(
        f'Loading Automated Archive file "{args.db_input_file}" into database "{args.temp_db_database}"'
    )
    aa.clean_and_load_data(args, log)
