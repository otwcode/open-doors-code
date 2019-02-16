# coding=utf-8
import os
from unittest import TestCase
import unittest

import MySQLdb

from eFiction.efiction import eFiction
from shared_python.Logging import logger
from shared_python.Sql import Sql
import argparse

from shared_python.Tags import Tags


def testArgs():
  parser = argparse.ArgumentParser(description='Test an archive database')
  args = parser.parse_args()
  setattr(args, "archive_type", "EF")
  setattr(args, "db_host", "localhost")
  setattr(args, "db_user", "root")
  setattr(args, "db_password", "")
  setattr(args, "temp_db_database", "unit_test")
  setattr(args, "db_input_file", os.path.join(os.path.dirname(__file__), "test_data/efiction.sql"))
  setattr(args, "output_database", "unit_test_output")
  return args

class TestEFiction(TestCase):
  args = testArgs()
  log = logger("test")
  sql = Sql(args, log)
  tags = Tags(args, sql.db, log)
  efiction = eFiction(args, sql, log, tags)
  efiction_db = "{0}_efiction".format(args.temp_db_database)

  @classmethod
  def setUpClass(cls):
    cls.efiction.load_database()
    cls.efiction.copy_tags_to_tags_table(None, "y")

  @classmethod
  def tearDownClass(cls):
    cls.sql.execute("DROP DATABASE IF EXISTS {0}".format(cls.efiction_db))
    cls.sql.execute("DROP DATABASE IF EXISTS {0}".format(cls.args.temp_db_database))

  def test_load_database(self):
    cursor = self.sql.cursor

    test_msg = "original efiction database name from the SQL file should not be created"
    cursor.execute("SHOW DATABASES LIKE 'test_efiction_original_database_name_we_dont_want'")
    unwanted_database = cursor.fetchone()
    self.assertEquals(None, unwanted_database, test_msg)

    test_msg = "fanfiction_authorfields table should contain the same number of records as in the SQL file"
    cursor.execute("SELECT COUNT(*) FROM {0}.fanfiction_authorfields".format(self.efiction_db))
    (authorfields,) = cursor.fetchone()
    self.assertEqual(3L, authorfields, test_msg)

  def test_copy_tags_to_tags_table(self):
    cursor = self.sql.db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT original_tag FROM {0}.tags".format(self.efiction_db))
    tags = list(cursor.fetchall())
    unique_tags = set(tag_dict['original_tag'] for tag_dict in tags)
    self.assertEqual(77L, len(tags), "tags table should be a denormalised table")
    self.assertIn(u'Václav', unique_tags, "tags table should contain the tags referenced in the story files as a denormalised table")

  def test_copy_to_temp_db(self):
    self.efiction.copy_to_temp_db(has_coauthors=True)
    cursor = self.sql.cursor
    cursor.execute("SELECT * FROM {0}.fanfiction_stories".format(self.efiction_db))
    original_stories = cursor.fetchall()
    cursor.execute("SELECT * FROM {0}.stories".format(self.args.temp_db_database))
    stories = cursor.fetchall()

    cursor.execute("SELECT * FROM {0}.fanfiction_chapters".format(self.efiction_db))
    original_chapters = cursor.fetchall()
    cursor.execute("SELECT * FROM {0}.chapters".format(self.args.temp_db_database))
    chapters = cursor.fetchall()

    cursor.execute("SELECT * FROM {0}.fanfiction_authors".format(self.efiction_db))
    original_authors = cursor.fetchall()
    cursor.execute("SELECT * FROM {0}.authors".format(self.args.temp_db_database))
    authors = cursor.fetchall()

    self.assertEqual(len(original_stories), len(stories), "temp db stories table should contain all the stories from the original efiction table")
    self.assertEqual(len(original_chapters), len(chapters), "temp db chapters table should contain all the chapters from the original efiction table")
    self.assertEqual(len(original_authors), len(authors), "temp db authors table should contain all the authors from the original efiction table")

if __name__ == '__main__':
  unittest.main()
