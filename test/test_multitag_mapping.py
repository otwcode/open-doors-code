from collections import defaultdict
from unittest import TestCase
import unittest
from unittest.mock import MagicMock
import pdb
from shared_python.Sql import Sql
from shared_python.Logging import logger
from shared_python.PopulateTags import PopulateTags
import argparse

from shared_python.Tags import Tags

def testArgs():
	parser = argparse.ArgumentParser(description='Test an archive database')
	args = parser.parse_args()
	setattr(args, "archive_type", "AA")
	setattr(args, "db_host", "localhost")
	setattr(args, "db_user", "root")
	setattr(args, "db_password", "")
	setattr(args, "temp_db_database", "test_working_open_doors")
	setattr(args, "output_database", "unit_test_output")
	setattr(args, "default_fandom", "Fandom C (TV)")
	return args

class TestMultiTagMapping(TestCase):
	args = testArgs()
	log = logger("test")
	sql = Sql(args, log)
	tags = Tags(args, sql, log)

	def test_multi_tag_mapping(self):

		row = {
			'Original Tag ID': '10', 
			'Original Tag': 'original-tag-1', 
			'Original Tag Type': 'classes', 
			'Original Parent Tag': 'Genres', 
			'Related Fandom': 'Fandom-1',
			'Recommended AO3 Tag': 'AO3-tag-1, AO3-tag-2, AO3-tag-3', 
			'Recommended AO3 Type': 'M/M, F/M',
			'Recommended AO3 Category (for relationships)': 'characters, tags, tags', 
			'Original Tag Description': '', 
			'TW Notes': ''
		}
		num_insert = self.tags.update_tag_row(row)
		self.assertEqual(num_insert, 4)

		row = {
			'Original Tag ID': '11', 
			'Original Tag': 'original-tag-2', 
			'Original Tag Type': 'classes', 
			'Original Parent Tag': 'Genres', 
			'Related Fandom': 'Fandom-2',
			'Recommended AO3 Tag': 'AO3-tag-2, AO3-tag-4', 
			'Recommended AO3 Type': 'M/M, F/M',
			'Recommended AO3 Category (for relationships)': 'fandoms, characters, tags', 
			'Original Tag Description': '', 
			'TW Notes': ''
		}
		num_insert = self.tags.update_tag_row(row)
		self.assertEqual(num_insert, 3)

if __name__ == '__main__':
  unittest.main()