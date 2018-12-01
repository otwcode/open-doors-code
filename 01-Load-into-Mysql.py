from shared_python import Args
from shared_python.Sql import Sql
from automated_archive import aa

import logging
import sys
logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
log = logging.getLogger()


if __name__ == "__main__":
  args = Args.args_for_01()
  sql = Sql(args)


# eg: python 01-Load-into-Mysql.py -dh localhost -du root -dt dsa -dd temp_python -a AA -f /path/to/ARCHIVE_DB.pl -o .
  if args.archive_type == 'AA':
    log.info('Loading Automated Archive file "{0}" into database "{1}"'.format(args.db_input_file, args.temp_db_database))
    aa.clean_and_load_data(args)

# eg: python 01-Load-into-Mysql.py -dh localhost -du root -dt sd -dd temp_python -a EF -f /path/to/backup-from-efiction.sql -o .
  elif args.archive_type == 'EF':
    log.info('Loading eFiction file "{0}" into database "{1}"'.format(args.db_input_file, args.temp_db_database))
    sql.run_script_from_file(args.db_input_file,
                             database = args.temp_db_database,
                             initial_load = True)
