# encoding: utf-8
import csv

import sys

from shared_python import Args
from shared_python.Sql import Sql
from shared_python.Tags import Tags

if __name__ == "__main__":
  args = Args.args_for_04()
  sql = Sql(args)
  tags = Tags(args, sql.db)

# Input CSV from TW spreadsheet
# Rename tags in `tags` table, populate ao3_tag_table column
  # eg: python 04-Rename-Tags.py -dh localhost -du root -dt dsa -dd temp_python -a EF -i path/to/tw-spreadsheet.csv

  with open(args.tag_input_file, 'r') as csvfile:
    tw_tags = list(csv.DictReader(csvfile))
    tag_headers = tags.tag_export_map
    total = len(tw_tags)

    for cur, row in enumerate(tw_tags):
      sys.stdout.write('\r{0}/{1} tags to map'.format(cur + 1, total))
      sys.stdout.flush()

      prefix = 'fanfiction' if args.archive_type == 'EF' else ''
      tags.update_tag_row(row, prefix)
