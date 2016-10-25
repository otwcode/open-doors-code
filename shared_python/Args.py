import os
import argparse


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
    'db_database': 'MySQL temporary database name to use for processing (will be destroyed if it exists)',
    'db_table_prefix': 'MySQL prefix for tables'
  }
  parser = argparse.ArgumentParser(description='Process an archive database')
  for name, helptext in argdict.items():
    parser.add_argument('-d' + name.split('_')[1][0], '--' + name, type=str, help=helptext)

  parser.add_argument('-a', '--archive_type', type=str, choices=['AA', 'EF'], help='Type of archive: AA or EF')
  parser.add_argument('-i', '--db_input_file', type=str, help='Path to input file (ARCHIVE_DB.pl for AA, SQL script for eFiction)')
  parser.add_argument('-o', '--output_folder', type=str, help='Path for output files')
  parser.add_argument('-t', '--tag_input_file', type=str, help='Path to tag renaming input CSV')
  parser.add_argument('-od', '--output_database', type=str, help='Name of the database the final tables should be created in (default "od_sgf")')

  parser.add_argument('-df', '--default_fandom', type=str, help='Default fandom to use')
  parser.add_argument('-cp', '--chapters_path', type=str, help='Location of the text files containing the stories')
  parser.add_argument('-cf', '--chapters_file_extensions', type=str, help='File extension(s) of the text files containing the stories (eg: "txt, html")')
  parser.add_argument('-n', '--archive_name', type=str, help='Name of the original archive (used in the temporary site)')
  parser.add_argument('-p', '--properties_file', type=str, help='Load properties from specified file (ignores all other arguments)')


  args = parser.parse_args()
  if args.properties_file is not None and os.path.isfile(args.properties_file):
    props = _load_args_from_file(args.properties_file)
    for k, v in props.items():
      if v == '':
        setattr(args, k, None)
      else:
        setattr(args, k, v)

  args.db_host = raw_input(argdict['db_host'] + ': ') if args.db_host is None else args.db_host
  args.db_user = raw_input(argdict['db_user'] + ': ') if args.db_user is None else args.db_user
  args.db_password = raw_input(argdict['db_password'] + ': ') if args.db_password is None else args.db_password
  args.db_database = raw_input(argdict['db_database'] + ': ') if args.db_database is None else args.db_database
  args.db_table_prefix = raw_input(argdict['db_table_prefix'] + ': ') if args.db_table_prefix is None else args.db_table_prefix
  args.archive_name = raw_input('Name of the original archive (used in export file names): ') if args.archive_name is None else args.archive_name

  while args.archive_type is None or args.archive_type not in ['AA', 'EF']:
    args.archive_type = raw_input('Type of archive (AA or EF): ')

  return args


def _print_args(args):
  print '----------- Open Door Archive Import Parameters --------------'
  for arg in vars(args):
    print '{0} = {1}'.format(arg, getattr(args, arg))
  print '--------------------------------------------------------------\n'


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
  _print_args(args)
  return args
