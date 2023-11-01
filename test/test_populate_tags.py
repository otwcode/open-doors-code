from unittest import TestCase
import unittest
from unittest.mock import MagicMock

from shared_python.Logging import logger
from shared_python.PopulateTags import PopulateTags
import argparse

from shared_python.Tags import Tags


def testArgs():
    parser = argparse.ArgumentParser(description="Test an archive database")
    args = parser.parse_args([])
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
    sql = MagicMock()
    tags = Tags(args, sql, log)
    final = MagicMock()
    populate_tags = PopulateTags(args, sql, log, tags, final)

    basic_tags = {
        "fandoms": [
            {"original_tag": "Fandom A", "ao3_tag": "Fandom A (TV)"},
            {"original_tag": "Fandom B", "ao3_tag": "Fandom B (TV)"},
        ],
        "tags": [{"original_tag": "a tag", "ao3_tag": "A Tag"}],
        "rating": [{"original_tag": "PG", "ao3_tag": "General Audiences"}],
        "warnings": [
            {"original_tag": "Violence", "ao3_tag": "Graphic Depictions Of Violence"}
        ],
    }

    def test_default_fandom_ignored_if_fandoms_present(self):
        story_tags = self.populate_tags.tags_for_story(1, self.basic_tags)
        self.assertCountEqual(
            ["Fandom A (TV)", "Fandom B (TV)"],
            story_tags["fandoms"].split(", "),
            "Fandoms should be a comma-separated string of specified AO3 tags",
        )

    def test_default_fandom_used_if_no_fandoms_present(self):
        tags_without_fandom = self.basic_tags.copy()
        tags_without_fandom.pop("fandoms")
        story_tags = self.populate_tags.tags_for_story(1, tags_without_fandom)
        self.assertEqual(
            "Fandom C (TV)",
            story_tags["fandoms"],
            "Fandoms should be a comma-separated string of specified AO3 tags",
        )

    def test_cntw_added_if_warnings_present(self):
        story_tags = self.populate_tags.tags_for_story(1, self.basic_tags)
        self.assertCountEqual(
            ["Graphic Depictions Of Violence", "Choose Not To Use Archive Warnings"],
            story_tags["warnings"].split(", "),
            "Warnings should be a comma-separated string of AO3 warnings that includes CNTW",
        )

    def test_cntw_added_if_no_warnings_present(self):
        tags_without_warnings = self.basic_tags.copy()
        tags_without_warnings.pop("warnings")
        story_tags = self.populate_tags.tags_for_story(1, tags_without_warnings)
        self.assertEqual(
            "Choose Not To Use Archive Warnings",
            story_tags["warnings"],
            "Warnings should be a comma-separated string of AO3 warnings that includes CNTW",
        )


if __name__ == "__main__":
    unittest.main()
