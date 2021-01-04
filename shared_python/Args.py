import os
import argparse
import yaml

from shared_python.Logging import logger

class Args(object):

  def __init__(self):
    self.args = self._process_args()
    self.log = logger(self.args.archive_name)

  def logger_with_filename(self):
    return self.log

  @staticmethod
  def _load_args_from_file(filepath):
    """
    Read the file passed as parameter as a properties file.
    """
    with open(filepath, "rt") as f:
      return yaml.safe_load(f)

  def _process_args(self):

    argdict = {
      'db_host': 'MySQL host name and port',
      'db_user': 'MySQL user',
      'db_password': 'MySQL password',
      'temp_db_database': 'MySQL temporary database name to use for processing (will be destroyed if it exists)',
    }
    parser = argparse.ArgumentParser(description='Process an archive database')
    for name, helptext in argdict.items():
      parser.add_argument('-d' + name.split('_')[1][0], '--' + name, type=str, help=helptext)

    # Pass in a file with all the properties
    parser.add_argument('-p', '--properties_file',           type=str, help='Load properties from specified file (ignores all other arguments)')

    # General archive-specific settings
    parser.add_argument('-a',  '--archive_type',             type=str, choices=['AA'], help='Type of archive: AA')
    parser.add_argument('-df', '--default_fandom',           type=str, help='Default fandom to use')
    parser.add_argument('-n',  '--archive_name',             type=str, help='Name of the original archive (used in the temporary site)')

    # Database settings
    parser.add_argument('-i',  '--db_input_file',            type=str, help='Path to input file (ARCHIVE_DB.pl for AA)')
    parser.add_argument('-o',  '--output_folder',            type=str, help='Path for output files')
    parser.add_argument('-od', '--output_database',          type=str, help='Name of the database the final tables should be created in (default "od_sgf")')

    # Tag settings
    parser.add_argument('-ft', '--tag_fields',               type=str, help='List of tag field(s) in original db (comma-delimited)')
    parser.add_argument('-fc', '--character_fields',         type=str, help='List of character field(s) in original db (comma-delimited)')
    parser.add_argument('-fr', '--relationship_fields',      type=str, help='List of relationship field(s) in original db (comma-delimited)')
    parser.add_argument('-ff', '--fandom_fields',            type=str, help='List of fandom field(s) in original db (comma-delimited)')
    parser.add_argument('-wf', '--fields_with_fandom',       type=str, help='List of output tag fields where the fandom should be listed too (comma-delimited)')

    # Wrangling and search processing
    parser.add_argument('-t',  '--tag_input_file',           type=str, help='Path to tag renaming input CSV')
    parser.add_argument('-si', '--story_ids_to_remove',      type=str, help='Location of the text file containing the story ids to remove')
    parser.add_argument('-bi', '--bookmark_ids_to_remove',   type=str, help='Location of the text file containing the bookmark ids to remove')

    # Chapters
    parser.add_argument('-cp', '--chapters_path',            type=str, help='Location of the text files containing the stories')
    parser.add_argument('-cf', '--chapters_file_extensions', type=str, help='File extension(s) of the text files containing the stories (eg: "txt, html")')


    args = parser.parse_args()
    if args.properties_file is not None and os.path.isfile(args.properties_file):
      props = self._load_args_from_file(args.properties_file)
      for k, v in props.items():
        if v == '':
          setattr(args, k, None)
        else:
          setattr(args, k, v)

    for arg_name in argdict.keys():
      if getattr(args, arg_name) is None:
        setattr(args, arg_name, input(argdict[arg_name] + ': '))

    args.archive_name =     input('Name of the original archive (used in export file names): ') if args.archive_name is None else args.archive_name

    while args.archive_type is None or args.archive_type not in ['AA']:
      args.archive_type = input('Type of archive (AA): ')

    return args


  def _print_args(self, args):
    self.log.info('----------- Open Door Archive Import Parameters --------------')
    for arg in vars(args):
      self.log.info('{0} = {1}'.format(arg, getattr(args, arg)))
    self.log.info('--------------------------------------------------------------')


  def args_for_01(self):
    while self.args.db_input_file is None or not os.path.isfile(self.args.db_input_file):
      self.args.db_input_file = input('Path to the input file (ARCHIVE_DB.pl for AA): ')
    self._print_args(self.args)
    return self.args


  def args_for_02(self):
    self._print_args(self.args)
    return self.args


  def args_for_03(self):
    if not os.path.exists(self.args.output_folder):
      os.makedirs(self.args.output_folder)
    while self.args.output_folder is None or not os.path.isdir(self.args.output_folder):
      self.args.output_folder = input('Path for output files: ')
      if not os.path.exists(self.args.output_folder):
        os.makedirs(self.args.output_folder)
    self._print_args(self.args)
    return self.args


  def args_for_04(self):
    while self.args.tag_input_file is None or not os.path.isfile(self.args.tag_input_file):
      self.args.tag_input_file = input('Path to tag renaming csv file: ')
    self._print_args(self.args)
    return self.args


  def args_for_05(self):
    if self.args.output_database is None:
      self.args.output_database = input('Name of the database the final tables should be created in (default "od_sgf"):')
      self.args.output_database = "od_sgf" if self.args.output_database is "" else self.args.output_database
    if self.args.story_ids_to_remove is None:
      self.args.story_ids_to_remove = input('Location of the text file containing the story ids to remove:')
    self._print_args(self.args)
    return self.args


  def args_for_06(self):
    if self.args.output_database is None:
      self.args.output_database = input('Name of the database the final tables should be created in (default "od_sgf"):')
    self.args.output_database = "od_sgf" if self.args.output_database is "" else self.args.output_database
    if self.args.default_fandom is None:
      self.args.default_fandom = input('Default fandom:')
      self.args.default_fandom = '' if self.args.default_fandom is None else self.args.default_fandom
    self._print_args(self.args)
    return self.args

  def args_for_07(self):
    if self.args.output_database is None:
      self.args.output_database = input('Name of the database the final tables should be created in (default "od_sgf"):')
      self.args.output_database = "od_sgf" if self.args.output_database is "" else self.args.output_database
    if self.args.chapters_path is None:
      self.args.chapters_path = input('Location of the text files containing the stories:')
    if self.args.chapters_path is not None and self.args.chapters_file_extensions is None:
      self.args.chapters_file_extensions = input('File extension(s) of the text files containing the stories (eg: "txt, html"):')
    self._print_args(self.args)
    return self.args
