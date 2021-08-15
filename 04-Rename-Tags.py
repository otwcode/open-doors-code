# encoding: utf-8
import csv

from shared_python.Args import Args
from shared_python.Common import print_progress
from shared_python.Sql import Sql
from shared_python.Tags import Tags


if __name__ == "__main__":
  """
  When Tag Wrangling have finished mapping the tags in Google Drive, export the spreadsheet as a CSV file. This script
  then copies the AO3 tags from that file into the tags table in the temporary database.
  """
  args_obj = Args()
  args = args_obj.args_for_04()
  log = args_obj.logger_with_filename()
  sql = Sql(args, log)
  tags = Tags(args, sql, log)

  with open(args.tag_input_file, 'r', encoding='utf-8-sig') as csvfile:
    tw_tags = list(csv.DictReader(csvfile))
    tag_headers = tags.tag_export_map
    total = len(tw_tags)

    for cur, row in enumerate(tw_tags):
      tags.update_tag_row(row)
      print_progress(cur, total, "tags")
