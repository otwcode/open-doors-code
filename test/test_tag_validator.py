import unittest
from unittest import TestCase
from unittest.mock import patch

from shared_python.Logging import logger
from shared_python.TagValidator import TagValidator

class testTag_Validator(TestCase):
    log = logger("test")
    tag_validator = TagValidator(log)

    # Tag Type Dictionary Tests
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

    # Rating Dictionary Tests
    def test_identify_rating_not_rated(self):
        tag = self.tag_validator.identify_rating("Not Rated")
        self.assertEqual(tag, 1, "rating Not Rated should be 1")

    def test_identify_rating_general_audiences(self):
        tag = self.tag_validator.identify_rating("General Audiences")
        self.assertEqual(tag, 2, "rating General Audiences should be 2")

    def test_identify_rating_teen_and_up(self):
        tag = self.tag_validator.identify_rating("Teen And Up Audiences")
        self.assertEqual(tag, 3, "rating Teen And Up Audiences should be 3")

    def test_identify_rating_mature(self):
        tag = self.tag_validator.identify_rating("Mature")
        self.assertEqual(tag, 4, "rating Mature should be 4")

    def test_identify_rating_explicit(self):
        tag = self.tag_validator.identify_rating("Explicit")
        self.assertEqual(tag, 5, "rating Explicit should be 5")

    def test_identify_rating_wrong_case(self):
        tag = self.tag_validator.identify_rating("mature")
        self.assertEqual(tag, 0, "rating mature should be 0")

    def test_identify_rating_wrong_word(self):
        tag = self.tag_validator.identify_rating("foobar")
        self.assertEqual(tag, 0, "rating foobar should be 0")

    # Warning Dictionary Tests
    def test_identify_warning_choose_no_archive_warnings(self):
        tag = self.tag_validator.identify_warning("Choose Not To Use Archive Warnings")
        self.assertEqual(tag, 1, "warning Choose Not To Use Archive Warnings should be 1")

    def test_identify_warning_graphic_violence(self):
        tag = self.tag_validator.identify_warning("Graphic Depictions Of Violence")
        self.assertEqual(tag, 2, "warning Graphic Depictions Of Violence should be 2")

    def test_identify_warning_major_char_death(self):
        tag = self.tag_validator.identify_warning("Major Character Death")
        self.assertEqual(tag, 3, "warning Major Character Death should be 3")

    def test_identify_warning_no_archive_warnings(self):
        tag = self.tag_validator.identify_warning("No Archive Warnings Apply")
        self.assertEqual(tag, 4, "warning No Archive Warnings Apply should be 4")

    def test_identify_warning_rape_noncon(self):
        tag = self.tag_validator.identify_warning("Rape/Non-Con")
        self.assertEqual(tag, 5, "warning Rape/Non-Con should be 5")

    def test_identify_warning_underage(self):
        tag = self.tag_validator.identify_warning("Underage")
        self.assertEqual(tag, 6, "warning Underage should be 6")

    def test_identify_warning_wrong_case(self):
        tag = self.tag_validator.identify_warning("underage")
        self.assertEqual(tag, 0, "warning underage should be 0")

    def test_identify_warning_wrong_word(self):
        tag = self.tag_validator.identify_warning("foobar")
        self.assertEqual(tag, 0, "warning foobar should be 0")

    # Category Dictionary Tests
    def test_identify_category_gen(self):
        tag = self.tag_validator.identify_category("Gen")
        self.assertEqual(tag, 1, "categories Gen should be 1")

    def test_identify_category_fm(self):
        tag = self.tag_validator.identify_category("F/M")
        self.assertEqual(tag, 2, "categories F/M should be 2")

    def test_identify_category_mm(self):
        tag = self.tag_validator.identify_category("M/M")
        self.assertEqual(tag, 3, "categories M/M should be 3")

    def test_identify_category_ff(self):
        tag = self.tag_validator.identify_category("F/F")
        self.assertEqual(tag, 4, "categories F/F should be 4")

    def test_identify_category_multi(self):
        tag = self.tag_validator.identify_category("Multi")
        self.assertEqual(tag, 5, "categories Multi should be 5")

    def test_identify_category_other(self):
        tag = self.tag_validator.identify_category("Other")
        self.assertEqual(tag, 6, "categories Other should be 6")

    def test_identify_category_wrong_case(self):
        tag = self.tag_validator.identify_category("multi")
        self.assertEqual(tag, 0, "categories multi should be 0")

    def test_identify_category_wrong_word(self):
        tag = self.tag_validator.identify_category("foobar")
        self.assertEqual(tag, 0, "categories foobar should be 0")

    # Validate and Fix Tag Type Tests: Pass with No Self Correction or Prompts
    def test_validate_and_fix_tag_type_rating(self):
        tag = self.tag_validator.validate_and_fix_tag_type("rating")
        self.assertEqual(tag, "rating", "rating should pass with no fixes")

    def test_validate_and_fix_tag_type_warnings(self):
        tag = self.tag_validator.validate_and_fix_tag_type("warnings")
        self.assertEqual(tag, "warnings", "warnings should pass with no fixes")

    def test_validate_and_fix_tag_type_categories(self):
        tag = self.tag_validator.validate_and_fix_tag_type("categories")
        self.assertEqual(tag, "categories", "categories should pass with no fixes")

    def test_validate_and_fix_tag_type_fandoms(self):
        tag = self.tag_validator.validate_and_fix_tag_type("fandoms")
        self.assertEqual(tag, "fandoms", "fandoms should pass with no fixes")

    def test_validate_and_fix_tag_type_characters(self):
        tag = self.tag_validator.validate_and_fix_tag_type("characters")
        self.assertEqual(tag, "characters", "characters should pass with no fixes")

    def test_validate_and_fix_tag_type_relationships(self):
        tag = self.tag_validator.validate_and_fix_tag_type("relationships")
        self.assertEqual(tag, "relationships", "relationships should pass with no fixes")

    def test_validate_and_fix_tag_type_tags(self):
        tag = self.tag_validator.validate_and_fix_tag_type("tags")
        self.assertEqual(tag, "tags", "tags should pass with no fixes")

    # Validate and Fix Tag Type Tests: Pass with Self Correction
    def test_validate_and_fix_tag_type_correct_missing_s(self):
        tag = self.tag_validator.validate_and_fix_tag_type("tag")
        self.assertEqual(tag, "tags", "tag should pass with successful self-correction")

    def test_validate_and_fix_tag_type_correct_extra_s(self):
        tag = self.tag_validator.validate_and_fix_tag_type("ratings")
        self.assertEqual(tag, "rating", "ratings should pass with successful self-correction")

    def test_validate_and_fix_tag_type_correct_wrong_case(self):
        tag = self.tag_validator.validate_and_fix_tag_type("Rating")
        self.assertEqual(tag, "rating", "Rating should pass with successful self-correction")

    def test_validate_and_fix_tag_type_correct_wrong_case_and_missing_s(self):
        tag = self.tag_validator.validate_and_fix_tag_type("Tag")
        self.assertEqual(tag, "tags", "Tag should pass with successful self-correction")

    def test_validate_and_fix_tag_type_correct_wrong_case_and_extra_s(self):
        tag = self.tag_validator.validate_and_fix_tag_type("Ratings")
        self.assertEqual(tag, "rating", "Ratings should pass with successful self-correction")

    # Validate and Fix Tag Type Tests: Pass with Prompts
    @patch('builtins.input', return_value='tags')
    def test_validate_and_fix_tag_type_one_prompt_no_selfcorrect(self, mock_input):
        tag = self.tag_validator.validate_and_fix_tag_type("foobar")
        self.assertEqual(tag, "tags", "foobar should prompt for manual correction without self-correction")

    @patch('builtins.input', return_value='tag')
    def test_validate_and_fix_tag_type_one_prompt_selfcorrect(self, mock_input):
        tag = self.tag_validator.validate_and_fix_tag_type("foobar")
        self.assertEqual(tag, "tags", "foobar should prompt for manual correct followed by self-correction")

    @patch('builtins.input', side_effect=['foo', 'facts', 'tag'])
    def test_validate_and_fix_tag_type_one_prompt_selfcorrect(self, mock_input):
        tag = self.tag_validator.validate_and_fix_tag_type("foobar")
        self.assertEqual(tag, "tags", "foobar should prompt for manual correction thrice with self-correction")

    # Validate and Fix Tag Tests: Pass with No Self Correction or Prompts
    def test_validate_and_fix_tag_rating(self):
        tag = self.tag_validator.validate_and_fix_tag("Not Rated", "rating")
        self.assertEqual(tag, "Not Rated", "Not Rated should pass with no fixes")

    def test_validate_and_fix_tag_warnings(self):
        tag = self.tag_validator.validate_and_fix_tag("Rape/Non-Con", "warnings")
        self.assertEqual(tag, "Rape/Non-Con", "Rape/Non-Con should pass with no fixes")

    def test_validate_and_fix_tag_categories(self):
        tag = self.tag_validator.validate_and_fix_tag("M/M", "categories")
        self.assertEqual(tag, "M/M", "M/M should pass with no fixes")

    def test_validate_and_fix_tag_other(self):
        tag = self.tag_validator.validate_and_fix_tag("Kirk/Spock", "relationships")
        self.assertEqual(tag, "Kirk/Spock", "Kirk/Spock should pass with no fixes")

    # Validate and Fix Tag Tests: Pass with Prompts
    @patch('builtins.input', return_value='Not Rated')
    def test_validate_and_fix_tag_type_one_prompt(self, mock_input):
        tag = self.tag_validator.validate_and_fix_tag("not ated", "rating")
        self.assertEqual(tag, "Not Rated", "not ated should prompt for manual correction to Not Rated")

    @patch('builtins.input', side_effect=['mlm', 'M/M'])
    def test_validate_and_fix_tag_two_prompts(self, mock_input):
        tag = self.tag_validator.validate_and_fix_tag("male x male", "categories")
        self.assertEqual(tag, "M/M", "male x male should prompt twice for manual correction to M/M")

if __name__ == '__main__':
  print('here')
  unittest.main()
