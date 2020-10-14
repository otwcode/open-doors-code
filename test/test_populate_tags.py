from collections import defaultdict
from unittest import TestCase
import unittest

from shared_python.FinalTables import FinalTables
from shared_python.Logging import logger
from shared_python.PopulateTags import PopulateTags
from shared_python.Sql import Sql
import argparse

from shared_python.Tags import Tags


def testArgs():
  parser = argparse.ArgumentParser(description='Test an archive database')
  args = parser.parse_args()
  setattr(args, "archive_type", "AA")
  setattr(args, "db_host", "localhost")
  setattr(args, "db_user", "root")
  setattr(args, "db_password", "")
  setattr(args, "temp_db_database", "unit_test")
  setattr(args, "output_database", "unit_test_output")
  setattr(args, "default_fandom", "Fandom C (TV)")
  return args

class TestPopulate_tags(TestCase):
  args = testArgs()
  log = logger("test")
  sql = Sql(args, log)
  tags = Tags(args, sql.db, log)
  final = FinalTables(args, sql.db, log)
  populate_tags = PopulateTags(args, sql, log, tags, final)

  basic_tags = {
    'fandoms': [
      {'original_tag': 'Fandom A', 'ao3_tag': 'Fandom A (TV)'},
      {'original_tag': 'Fandom B', 'ao3_tag': 'Fandom B (TV)'}
    ],
    'tags': [
      {'original_tag': 'a tag', 'ao3_tag': 'A Tag'}
    ],
    'rating': [{'original_tag': 'PG', 'ao3_tag': 'General Audiences'}]
  }

  def test_default_fandom_ignored_if_fandoms_present(self):
    story_tags = self.populate_tags.tags_for_story(1, self.basic_tags)
    self.assertEqual('Fandom A (TV), Fandom B (TV)', story_tags['fandoms'], 'Fandoms should be a comma-separated string of specified AO3 tags')

  def test_default_fandom_used_if_no_fandoms_present(self):
    tags_without_fandom = self.basic_tags.copy()
    tags_without_fandom.pop('fandoms')
    story_tags = self.populate_tags.tags_for_story(1, tags_without_fandom)
    self.assertEqual('Fandom C (TV)', story_tags['fandoms'], 'Fandoms should be a comma-separated string of specified AO3 tags')


if __name__ == '__main__':
  unittest.main()
