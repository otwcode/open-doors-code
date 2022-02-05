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
	parser = argparse.ArgumentParser(description='Test an archive database')
	args = parser.parse_args()
	setattr(args, "archive_type", "AA")
	setattr(args, "db_host", "localhost")
	setattr(args, "db_user", "root")
	setattr(args, "db_password", "test")
	setattr(args, "temp_db_database", "test_final_open_doors")
	setattr(args, "output_database", "test_final_open_doors")
	setattr(args, "default_fandom", "Fandom C (TV)")
	setattr(args, "sql_path", "./shared_python/create-open-doors-tables.sql")
	return args

class TestTagsLength(TestCase):
	args = testArgs()
	log = logger("test")
	sql = Sql(args, log)
	sql.execute("DROP DATABASE IF EXISTS test_final_open_doors;")
	sql.run_script_from_file(args.sql_path, args.temp_db_database, initial_load=False)
	final_tables = FinalTables(args, sql, log)

	def test_tags_length(self):
		
		test_item = [
			{	'id': 1, 
				'title': 'story title', 
				'summary ': '<p>story summary</p>', 
				'notes': '', 
				'author_id': 2, 
				'date': datetime.datetime(2022, 9, 4, 22, 38, 47), 
				'updated': datetime.datetime(2022, 9, 4, 22, 38, 47), 
				'url': None, 
				'ao3_url': None, 
				'imported': 0, 
				'do_not_import': 0, 
				'coauthor_id': None
				}
			]
		long_tags = """Previous code fails to process tags longer than 255 chars. 
									This is a long test tags with length greater than 255 chars. 
									This is a long test tags with length greater than 255 chars. 
									This is a long test tags with length greater than 255 chars. 
									This is a long test tags with length greater than 255 chars."""
		story_tags = {'categories': 'M/M', 
									'fandoms': 'This is a fandom', 
									'rating': 'Explicit', 
									'tags': long_tags, 
									'relationships': 'AAA/BBB'}
		story_id = 1
		output_table_name = "stories"
		self.final_tables.insert_into_final(output_table_name, test_item)
		self.final_tables.populate_story_tags(story_id, output_table_name, story_tags)
		
		extract_summary = self.sql.execute_and_fetchall(self.args.temp_db_database,
                              f"""SELECT tags FROM stories""")
		self.assertEqual(extract_summary[0][0], long_tags)

if __name__ == '__main__':
  unittest.main()