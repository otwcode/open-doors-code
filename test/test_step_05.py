import argparse
import importlib
import os
import sys
import unittest
from collections import defaultdict
from unittest import TestCase

from shared_python.Logging import logger
from shared_python.Sql import Sql

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

step_05 = importlib.import_module("05-Create-Open-Doors-Tables")


def testArgs():
    parser = argparse.ArgumentParser(description="Test an archive database")
    args = parser.parse_args()
    args.archive_type = "AA"
    args.db_host = "localhost"
    args.db_user = "root"
    args.db_password = "test"
    args.temp_db_database = "test_working_step_five"
    args.output_database = "unit_test_step_five"
    args.default_fandom = "Fandom C (TV)"
    args.sql_path = "./test/test_data/test_working_tables.sql"
    args.story_ids_to_remove = ""
    args.bookmark_ids_to_remove = ""
    return args


class TestStepFive(TestCase):
    args = testArgs()
    log = logger("test")
    sql = Sql(args, log)
    sql.run_script_from_file(args.sql_path, args.temp_db_database, initial_load=False)

    def test_chapter_table_structure(self):
        step_05.main(self.args, self.log)

        get_indexes = f"show index from {self.args.output_database}.chapters"
        result = self.sql.execute_dict(get_indexes)

        col_indexes = defaultdict(list)
        for index in result:
            col_indexes[index["Column_name"]].append(index)
        self.assertGreaterEqual(len(col_indexes["id"]), 1)
        self.assertEqual(len(col_indexes["story_id"]), 1)

    def tearDown(self):
        drop_working = f"drop database {self.args.temp_db_database}"
        self.sql.execute(drop_working, database=self.args.temp_db_database)
        drop_final = f"drop database {self.args.output_database}"
        self.sql.execute(drop_final, database=self.args.output_database)


if __name__ == "__main__":
    unittest.main()
