# encoding: utf-8
from shared_python.Args import Args
from shared_python.FinalTables import FinalTables
from shared_python.PopulateTags import PopulateTags
from shared_python.Sql import Sql
from shared_python.Tags import Tags


if __name__ == "__main__":
  """
  Denormalize tags out of the working tags table into comma-separated lists in the stories or story_link tables
  """
  args_obj = Args()
  args = args_obj.args_for_06()
  log = args_obj.logger_with_filename()
  sql = Sql(args, log)
  tags = Tags(args, sql, log)
  final = FinalTables(args, sql, log)
  populate_tags = PopulateTags(args, sql, log, tags, final)

  populate_tags.populate_tags()