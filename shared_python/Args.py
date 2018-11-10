import logging
import os
import argparse

log = logging.getLogger()

def _load_args_from_file(filepath):
  """
  Read the file passed as parameter as a properties file.
  """
  props = {}
  sep = ':'
  with open(filepath, "rt") as f:
    for line in f:
      l = line.strip()
      if l:
        key_value = l.split(sep)
        key = key_value[0].strip()
        value = sep.join(key_value[1:]).strip().strip('"')
        props[key] = value
  return props


def _process_args():

  argdict = {
    'db_host': 'MySQL host name and port',
    'db_user': 'MySQL user',
    'db_password': 'MySQL password',
    'temp_db_database': 'MySQL temporary database name to use for processing (will be destroyed if it exists)',
    'db_table_prefix': 'MySQL prefix for tables'
  }
  parser = argparse.ArgumentParser(description='Process an archive database')
  for name, helptext in argdict.items():
    parser.add_argument('-d' + name.split('_')[1][0], '--' + name, type=str, help=helptext)

  # Pass in a file with all the properties
  parser.add_argument('-p', '--properties_file',           type=str, help='Load properties from specified file (ignores all other arguments)')

  # General archive-specific settings
  parser.add_argument('-a',  '--archive_type',             type=str, choices=['AA', 'EF'], help='Type of archive: AA or EF')
  parser.add_argument('-df', '--default_fandom',           type=str, help='Default fandom to use')
  parser.add_argument('-n',  '--archive_name',             type=str, help='Name of the original archive (used in the temporary site)')

  # Database settings
  parser.add_argument('-i',  '--db_input_file',            type=str, help='Path to input file (ARCHIVE_DB.pl for AA, SQL script for eFiction)')
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
    props = _load_args_from_file(args.properties_file)
    for k, v in props.items():
      if v == '':
        setattr(args, k, None)
      else:
        setattr(args, k, v)

  for arg_name in argdict.keys():
    if getattr(args, arg_name) is None:
      setattr(args, arg_name, raw_input(argdict[arg_name] + ': '))

  args.archive_name =     raw_input('Name of the original archive (used in export file names): ') if args.archive_name is None else args.archive_name

  while args.archive_type is None or args.archive_type not in ['AA', 'EF']:
    args.archive_type = raw_input('Type of archive (AA or EF): ')

  return args


def _print_args(args):
  log.info('----------- Open Door Archive Import Parameters --------------')
  for arg in vars(args):
    log.info('{0} = {1}'.format(arg, getattr(args, arg)))
  log.info('--------------------------------------------------------------')


def args_for_01():
  args = _process_args()
  while args.db_input_file is None or not os.path.isfile(args.db_input_file):
    args.db_input_file = raw_input('Path to the input file (ARCHIVE_DB.pl for AA, SQL script for eFiction): ')
  _print_args(args)
  return args


def args_for_02():
  args = _process_args()
  _print_args(args)
  return args


def args_for_03():
  args = _process_args()
  if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)
  while args.output_folder is None or not os.path.isdir(args.output_folder):
    args.output_folder = raw_input('Path for output files: ')
    if not os.path.exists(args.output_folder):
      os.makedirs(args.output_folder)
  _print_args(args)
  return args


def args_for_04():
  args = _process_args()
  while args.tag_input_file is None or not os.path.isfile(args.tag_input_file):
    args.tag_input_file = raw_input('Path to tag renaming csv file: ')
  _print_args(args)
  return args


def args_for_05():
  args = _process_args()
  if args.output_database is None:
    args.output_database = raw_input('Name of the database the final tables should be created in (default "od_sgf"):')
    args.output_database = "od_sgf" if args.output_database is "" else args.output_database
  if args.chapters_path is None:
    args.chapters_path = raw_input('Location of the text files containing the stories:')
  if args.chapters_path is not None and args.chapters_file_extensions is None:
    args.chapters_file_extensions = raw_input('File extension(s) of the text files containing the stories (eg: "txt, html"):')
  _print_args(args)
  return args

def args_for_06():
  args = _process_args()
  if args.output_database is None:
    args.output_database = raw_input('Name of the database the final tables should be created in (default "od_sgf"):')
  args.output_database = "od_sgf" if args.output_database is "" else args.output_database
  if args.default_fandom is None:
    args.default_fandom = raw_input('Default fandom:')
    args.default_fandom = '' if args.default_fandom is None else args.default_fandom
  if args.story_ids_to_remove is None:
    args.story_ids_to_remove = raw_input('Location of the text file containing the story ids to remove:')
  _print_args(args)
  return args
