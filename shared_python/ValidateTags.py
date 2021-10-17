from logging import Logger

class ValidateTags(object):
    def __init__(self, log):
        self.log = log

    ## Dictionaries for tag validation
    dict_tag_type = {
        "rating": 1,
        "warnings": 2,
        "categories": 3,
        "fandoms": 4,
        "characters": 5,
        "relationships": 6,
        "tags": 7
    }
    dict_rating = {
        "Not Rated": 1,
        "General Audiences": 2,
        "Teen And Up Audiences": 3,
        "Mature": 4,
        "Explicit": 5
    }
    dict_warning = {
        "Choose Not To Use Archive Warnings": 1,
        "Graphic Depictions Of Violence": 2,
        "Major Character Death": 3,
        "No Archive Warnings Apply": 4,
        "Rape/Non-Con": 5,
        "Underage": 6
    }
    dict_category = {
        "Gen": 1,
        "F/M": 2,
        "M/M": 3,
        "F/F": 4,
        "Multi": 5,
        "Other": 6
    }

    ## Functions for accessing dictionaries
    def identify_tag_type(self, tag_type):
        return self.dict_tag_type.get(tag_type, 0)

    def identify_rating(self, tag):
        return self.dict_rating.get(tag, 0)

    def identify_warning(self, tag):
        return self.dict_warning.get(tag, 0)

    def identify_category(self, tag):
        return self.dict_category.get(tag, 0)

    ## Print statements
    def print_tag_correction(self, before, after):
        print('\r\033[96m', end='')
        self.log.info('Correction successful. "' + before + '" is now "' + after+ '"')
        print('\x1b[0m', end='')

    def print_tag_warning(self, tag, isType):
        print('\r\033[93m', end='')
        if (isType):
            self.log.warning('Warning: "' + tag + '" is not a valid TAG TYPE. Attempting self correction...')
        else:
            self.log.warning('Warning: "' + tag + '" is not a valid TAG. Attempting self correction...')
        print('\x1b[0m', end='')

    def print_fail_self(self):
        print('\r\033[91m', end='')
        self.log.warning('All attempts at self correction have failed. Manual correction required.')
        print('\x1b[0m', end='')

    def print_fail(self, tag_name):
        print('\r\033[91m', end='')
        if (tag_name):
            self.log.warning('Manual Input Failed. "' + tag_name + '" has failed re-check.')
        else:
            self.log.warning('Manual Input Failed. This field cannot be empty.')
        print('\x1b[0m', end='')

    def prompt_correction(self, tag_name, tag_type, isType):
        print ('\r\033[91mThe following values are accepted:\x1b[0m')
        if (isType):
            print('\r\033[91m' + self.list_dicts(None, tag_type) + '\x1b[0m')
        else:
            print('\r\033[91m' + self.list_dicts(tag_name, tag_type) + '\x1b[0m')
        prompt = '\r\033[91mPlease enter the correct name for "' + tag_name + '"'
        if (isType):
            prompt += ' (Press ENTER to default to "tags"):\x1b[0m '
        else:
            prompt += ':\x1b[0m '
        tag_correction = input(prompt)
        if (isType and not tag_correction):
            tag_correction = "tags"
        return tag_correction

    ## Self Correction Logic
    ## NOTE: This is for very light corrections only.
    def correct_tag_type(self, tag_type):
        # Attempt self correciton by making whole word lowercase
        tag_correction = tag_type.lower()
        if (self.classify_tag(None, tag_correction) > 0):
          self.print_tag_correction(tag_type, tag_correction)
          return tag_correction

        # Attempt self correction by adding last character
        if (self.classify_tag(None, tag_correction + "s") > 0):
          self.print_tag_correction(tag_type, tag_correction + "s")
          return tag_correction + "s"

        # Attempt self correction by removing last character
        if (self.classify_tag(None, tag_correction[:-1]) > 0):
          self.print_tag_correction(tag_type, tag_correction[:-1])
          return tag_correction[:-1]

        #All attempts failed
        return None

    def correct_tag(self, tag, tag_type):
        # Attempt self correction by uppercasing every first character
        if (self.classify_tag(tag.title(), tag_type) > 0):
            self.print_tag_correction(tag, tag.title())
            return tag.title()

        # All attempts failed
        return None

    ## Gating/Switch Logic
    def classify_tag(self, tag, tag_type):
        if (not tag):
            return self.identify_tag_type(tag_type)
        if (tag_type == "rating"):
            return self.identify_rating(tag)
        if (tag_type == "categories"):
            return self.identify_category(tag)
        if (tag_type == "warnings"):
            return self.identify_warning(tag)
        return 20

    def list_dicts(self, tag, tag_type):
        if (not tag):
            return str(list(self.dict_tag_type.keys()))
        elif (tag_type == 'rating'):
            return str(list(self.dict_rating.keys()))
        elif (tag_type == 'categories'):
            return str(list(self.dict_category.keys()))
        elif (tag_type == 'warnings'):
            return str(list(self.dict_warning.keys()))

    ## Verify methods to use
    def verify_tag_type(self, tag_type):
        if (self.classify_tag(None, tag_type) < 1):
          self.print_tag_warning(tag_type, True)

          # Attempt self correction
          tag_correction = self.correct_tag_type(tag_type)
          if (tag_correction):
              return tag_correction

          # Prompt and return for manual correction.
          self.print_fail_self()
          tag_correction = self.prompt_correction(tag_type, None, True)
          while (self.classify_tag(None, tag_correction) < 1):
              self.print_fail(tag_correction)
              tag_correction = self.prompt_correction(tag_type, None, True)
          self.print_tag_correction(tag_type, tag_correction)
          return tag_correction
        return tag_type

    def verify_tag(self, tag, tag_type):
        if (self.classify_tag(tag, tag_type) > 0):
            return tag
        self.print_tag_warning(tag, False)

        # Attempt self correction
        tag_correction = self.correct_tag(tag, tag_type)
        if (tag_correction):
            return tag_correction

        # Else prompt and return manual correction
        self.print_fail_self()
        tag_correction = self.prompt_correction(tag, tag_type, False)
        while (not tag_correction or self.classify_tag(tag_correction, tag_type) < 1):
            self.print_fail(tag_correction)
            tag_correction = self.prompt_correction(tag, tag_type, False)
        self.print_tag_correction(tag, tag_correction)
        return tag_correction