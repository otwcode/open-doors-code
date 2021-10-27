from unittest import TestCase
import unittest
# opendoors = __import__('open-doors-code')

from shared_python.Logging import logger
from shared_python.TagValidator import TagValidator

class testTag_Validator(TestCase):
    log = logger("test")
    tag_validator = TagValidator(log)

    # Tag Dictionary Tests
    def test_identify_tag_type_rating(self):
        tag_type = self.tag_validator.identify_tag_type("rating")
        self.assertEqual(tag_type, 1, "tag type rating should be 1")
    def test_identify_tag_type_warnings(self):
        tag_type = self.tag_validator.identify_tag_type("warnings")
        self.assertEqual(tag_type, 2, "tag type warnings should be 2")
    def test_identify_tag_type_categoryies(self):
        tag_type = self.tag_validator.identify_tag_type("categories")
        self.assertEqual(tag_type, 3, "tag type categories should be 3")
    def test_identify_tag_type_fandoms(self):
        tag_type = self.tag_validator.identify_tag_type("fandoms")
        self.assertEqual(tag_type, 4, "tag type fandoms should be 4")
    def test_identify_tag_type_characters(self):
        tag_type = self.tag_validator.identify_tag_type("characters")
        self.assertEqual(tag_type, 5, "tag type characters should be 5")
    def test_identify_tag_type_relationships(self):
        tag_type = self.tag_validator.identify_tag_type("relationships")
        self.assertEqual(tag_type, 6, "tag type relationships should be 6")
    def test_identify_tag_type_tags(self):
        tag_type = self.tag_validator.identify_tag_type("tags")
        self.assertEqual(tag_type, 7, "tag type tags should be 7")
    def test_identify_tag_type_wrong_case(self):
        tag_type = self.tag_validator.identify_tag_type("Rating")
        self.assertEqual(tag_type, 0, "tag type Rating should be 0")
    def test_identify_tag_type_wrong_word(self):
        tag_type = self.tag_validator.identify_tag_type("foobar")
        self.assertEqual(tag_type, 0, "tag type foobar should be 0")



if __name__ == '__main__':
  print('here')
  unittest.main()
