from collections import defaultdict
from unittest import TestCase
import unittest
from unittest.mock import MagicMock
from shared_python.Sql import Sql
from shared_python.Logging import logger
from shared_python.FinalTables import FinalTables
import argparse
import datetime

def testArgs():
	args = argparse.Namespace()
	setattr(args, "temp_db_database", "test_final_open_doors")
	setattr(args, "output_database", "test_final_open_doors")
	return args

class TestMultipleAuthors(TestCase):
	args = testArgs()
	log = logger("test")
	sql = None
	final_tables = FinalTables(args, sql, log)

	def test_multiple_authors(self):
		
		story = {'id': 1, 'title': 'A Story', 
						 'summary': "summary", 
						 'notes': '', 
						 'date': datetime.datetime(2022, 2, 27, 15, 48, 28), 
						 'updated': datetime.datetime(2022, 4, 15, 22, 4, 47), 
						 'categories': None, 
						 'tags': '', 'warnings': '', 
						 'fandoms': '', 
						 'characters': '', 
						 'relationships': '', 'language_code': '', 
						 'url': None, 'imported': 0, 'do_not_import': 0, 'ao3_url': None, 'import_notes': ''}

		story_authors = [{'id': 4114, 'author_id': 1, 'item_id': 1, 'item_type': 'story'}, {'id': 4115, 'author_id': 2, 'item_id': 1, 'item_type': 'story'}, {'id': 4116, 'author_id': 3, 'item_id': 1, 'item_type': 'story'}, {'id': 4117, 'author_id': 4, 'item_id': 1, 'item_type': 'story'}, {'id': 5, 'author_id': 5, 'item_id': 1, 'item_type': 'story'}, {'id': 4119, 'author_id': 6, 'item_id': 1, 'item_type': 'story'}, {'id': 4120, 'author_id': 7, 'item_id': 1, 'item_type': 'story'}, {'id': 4121, 'author_id': 8, 'item_id': 1, 'item_type': 'story'}, {'id': 4122, 'author_id': 9, 'item_id': 1, 'item_type': 'story'}]
		output_table_name = "stories"
		
		final_story = self.final_tables.story_to_final_without_tags(story, story_authors)
		self.assertEqual(final_story['notes'], 'Creators: 1, 2, 3, 4, 5, 6, 7, 8 and 9')

if __name__ == '__main__':
  unittest.main()