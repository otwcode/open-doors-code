# encoding: utf-8
import csv
import os

from eFiction import efiction
from shared_python import Args
from shared_python.Chapters import Chapters
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_05()
  sql = Sql(args)

  filter = 'WHERE `id` in '

  story_exclusion_filter = ''
  # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
  if os.path.exists(args.story_ids_to_remove):
    with open(args.story_ids_to_remove, "rt") as f:
      for line in f:
        story_exclusion_filter = filter + '(' + line + ')'

  command = "SET SQLDELETE FROM `{0}`.`stories` {2}".format(args.output_database, story_exclusion_filter)
  print command
  result = sql.execute(command)
  print result
