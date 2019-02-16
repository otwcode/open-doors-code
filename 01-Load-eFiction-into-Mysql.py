from eFiction import efiction
from shared_python.Args import Args
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args().args_for_01()
  log = args.logger_with_filename()
  sql = Sql(args, log)
  tags = Tags(args, sql.db, log)
  efiction = efiction.eFiction(args, sql, log, tags)

  efiction.convert_efiction_to_temp()