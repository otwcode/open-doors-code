from shared_python import Args
from shared_python.Sql import Sql
from automated_archive import aa

if __name__ == "__main__":
  args = Args.args_for_01()
  log = args.logger_with_filename()
  sql = Sql(args)

  # eg: python 01-Load-Automated-Archive-into-Mysql.py -dh localhost -du root -dt dsa -dd temp_python -a AA -f /path/to/ARCHIVE_DB.pl -o .
  log.info('Loading custom archive file "{0}" into database "{1}"'.format(args.db_input_file, args.temp_db_database))
  aa.clean_and_load_data(args, log)

