from logging import Logger

class TagValidator(object):
    def __init__(self, log):
        self.log = log

    ## Dictionaries/constants for tag validation
    IS_TAGTYPE = True
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
        self.log.info('Correction successful. "' + before + '" is now "' + after+ '"')

    def print_tag_warning(self, tag, tag_type, isType):
        if (isType):
            self.log.warning('Warning: "' + tag + '" is not a valid TAG TYPE.'
            + ' Attempting self correction...')
        else:
            self.log.warning('Warning: "' + tag + '" is not a valid '
            + tag_type.upper() + ' tag. Attempting self correction...')

    def print_fail_self(self):
        self.log.error('All attempts at self correction have failed.'
        + ' Manual correction required.')

    def print_fail(self, tag_name):
        if (tag_name):
            self.log.error('Manual Input Failed. "' + tag_name + '" has failed re-check.')
        else:
            self.log.error('Manual Input Failed. This field cannot be empty.')

    def prompt_correction(self, tag_name, tag_type, isType):
        print ('\rThe following values are accepted:')
        if (isType):
            print('\r' + self.list_dicts(None, tag_type))
        else:
            print('\r' + self.list_dicts(tag_name, tag_type))
        prompt = '\rPlease enter the correct name for "' + tag_name + '"'
        if (isType):
            prompt += ' (Press ENTER to default to "tags"): '
        else:
            prompt += ': '
        tag_correction = input(prompt)
        if (isType and not tag_correction):
            tag_correction = "tags"
        return tag_correction

    ## Self Correction Logic
    ## NOTE: This is for very light corrections only.
    def correct_tag_type(self, tag_type):
        # Attempt self correction by making whole word lowercase
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
        if (not tag):
            return None

        # Attempt self correction by uppercasing every first character
        tag_correction = tag.title()
        if (self.classify_tag(tag_correction, tag_type) > 0):
            self.print_tag_correction(tag, tag_correction)
            return tag_correction

        # Attempt self correction by replacing ampersands with 'and'
        tag_correction = tag.replace("&", "And")
        if (self.classify_tag(tag_correction, tag_type) > 0):
            self.print_tag_correction(tag, tag_correction)
            return tag_correction

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

    ## Validate methods to use.
    def validate_and_fix_tag_type(self, tag_type):
        if (self.classify_tag(None, tag_type) < 1):
          print()
          self.print_tag_warning(tag_type, None, True)

          # Attempt self correction
          tag_correction = self.correct_tag_type(tag_type)
          if (tag_correction):
              return tag_correction

          # Prompt manual correction.
          self.print_fail_self()
          tag_correction = self.prompt_correction(tag_type, None, self.IS_TAGTYPE)
          while (self.classify_tag(None, tag_correction) < 1):
              self.print_tag_warning(tag_correction, None, True)
              # Attempt correction of failed manual correction
              tag_selfcorrect = self.correct_tag_type(tag_correction)
              if (tag_selfcorrect):
                  self.print_tag_correction(tag_type, tag_selfcorrect)
                  return tag_selfcorrect
              # Else prompt manual correction again
              self.print_fail(tag_type)
              tag_correction = self.prompt_correction(tag_type, None, self.IS_TAGTYPE)
          self.print_tag_correction(tag_type, tag_correction)
          return tag_correction
        return tag_type

    def validate_and_fix_tag(self, tag, tag_type):
        if (self.classify_tag(tag, tag_type) > 0):
            return tag
        self.print_tag_warning(tag, tag_type, False)

        # Attempt self correction
        tag_correction = self.correct_tag(tag, tag_type)
        if (tag_correction):
            return tag_correction

        # Else prompt and return manual correction
        self.print_fail_self()
        tag_correction = self.prompt_correction(tag, tag_type, not self.IS_TAGTYPE)
        while (not tag_correction or self.classify_tag(tag_correction, tag_type) < 1):
            self.print_tag_warning(tag_correction, tag_type, False)
            # Attempt correction of failed manual correction
            tag_selfcorrect = self.correct_tag(tag_correction, tag_type)
            if (tag_selfcorrect):
                self.print_tag_correction(tag, tag_selfcorrect)
                return tag_selfcorrect
            # Else prompt manual correction again
            self.print_fail(tag_correction)
            tag_correction = self.prompt_correction(tag, tag_type, not self.IS_TAGTYPE)
        self.print_tag_correction(tag, tag_correction)
        return tag_correction
