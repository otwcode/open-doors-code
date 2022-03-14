# encoding: utf-8
import csv
import os

from shared_python.Args import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args_obj = Args()
  args = args_obj.args_for_05()
  log = args_obj.logger_with_filename()
  sql = Sql(args, log)

  filter = 'WHERE `id` in '

  story_exclusion_filter = ''
  # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
  if os.path.exists(args.story_ids_to_remove):
    with open(args.story_ids_to_remove, "rt") as f:
      for line in f:
        story_exclusion_filter = filter + '(' + line + ')'

  command = "DELETE FROM `{}`.`stories` {}".format(args.output_database, story_exclusion_filter)
  print(command)
  result = sql.execute(command)
  print(result)
