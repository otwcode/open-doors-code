from unittest import TestCase
import unittest

from shared_python.Logging import logger
from shared_python.TagValidator import TagValidator

class testTag_Validator(testCase):
    log = logger("test")
    tag_validator = TagValidator(log)

    # TODO: Tag Tests Here

if __name__ == '__main__':
  unittest.main()
