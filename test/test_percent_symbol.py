import argparse
import datetime
import unittest
from unittest import TestCase

from shared_python.FinalTables import FinalTables
from shared_python.Logging import logger
from shared_python.Sql import Sql


def testArgs():
    parser = argparse.ArgumentParser(description="Test an archive database")
    args = parser.parse_args()
    args.archive_type = "AA"
    args.db_host = "localhost"
    args.db_user = "root"
    args.db_password = "test"
    args.temp_db_database = "test_final_open_doors"
    args.output_database = "test_final_open_doors"
    args.default_fandom = "Fandom C (TV)"
    args.sql_path = "./test/test_data/test_final_tables.sql"
    return args


class TestPercentSymbol(TestCase):
    args = testArgs()
    log = logger("test")
    sql = Sql(args, log)
    sql.run_script_from_file(args.sql_path, args.temp_db_database, initial_load=False)
    final_tables = FinalTables(args, sql, log)

    def test_percent_symbol(self):
        test_item = [
            {
                "id": 1,
                "title": "story title",
                "summary ": "<p>This is a story summary with percent % symobol</p>",
                "notes": "",
                "author_id": 2,
                "date": datetime.datetime(2022, 9, 4, 22, 38, 47),
                "updated": datetime.datetime(2022, 9, 4, 22, 38, 47),
                "url": None,
                "ao3_url": None,
                "imported": 0,
                "do_not_import": 0,
                "coauthor_id": None,
            }
        ]
        self.final_tables.insert_into_final("stories", test_item)
        extract_summary = self.sql.execute_and_fetchall(
            self.args.temp_db_database, """SELECT summary FROM stories"""
        )

        self.assertEqual(
            extract_summary[0][0],
            "<p>This is a story summary with percent % symobol</p>",
        )


if __name__ == "__main__":
    unittest.main()
