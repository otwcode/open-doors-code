# -- coding: utf-8 --

import datetime
import codecs
import MySQLdb
import re
from HTMLParser import HTMLParser
from shared_python import Args, Common
from shared_python.Sql import Sql


def _clean_file(filepath):
  '''
  Convert the Perl hash into a Python dictionary
  :param filepath: Path to ARCHIVE_DB.pl
  :return: Python dictionary keyed by original story id
  '''
  h = HTMLParser()
  archive_db = codecs.open(filepath, 'r', encoding='utf-8').read()

  step1 = h.unescape(archive_db.replace('&#39;', '\\&#39;'))

  # Manually escape single quote entity and reformat file as a Python dictionary
  step2 = (
    step1
      .replace('%FILES = (\n\n', '{\n"').replace('\n)', '\n}')
      .replace('},\n', '},\n"').replace('\t', '    "')
      .replace(' =>', '":').replace(';', ',')
      .replace(',\n"\n},\n1,', '}')
  )
  # Replace line breaks within fields (followed by a character that isn't a space, tab, digit, } or ")
  step3 = re.sub(r"\n(?=[^ \t\d\}\"])", " ", step2)

  # Edit these to fix dodgy data specific to this archive
  final_replace = step3.replace("0,/2,/25", "01/30/00").replace('    "PrintTime": \'P\',\n', "")
  final_regex = re.sub(r"00,02,\d(.*?)',", "02/26/00',", final_replace)

  return eval(final_regex)


def _has_file_type(record):
  print("FileType: {0}".format(record.get('FileType', 'none') == 'none'))
  print("LocationURL: {0}".format(record.get('LocationURL', '').startswith('http')))
  return record.get('FileType', 'none') == 'none' or record.get('LocationURL', '').startswith('http')


def _create_mysql(args, FILES):
  db = MySQLdb.connect(args.db_host, args.db_user, args.db_password, "")
  cursor = db.cursor()
  DATABASE_NAME = args.temp_db_database
  PREFIX = args.db_table_prefix

  # Use the database and empty all the tables
  cursor.execute(u"drop database if exists {0};".format(DATABASE_NAME))
  cursor.execute(u"create database {0};".format(DATABASE_NAME))
  cursor.execute(u"use {0}".format(DATABASE_NAME))

  sql = Sql(args)
  sql.run_script_from_file('shared_python/create-open-doors-tables.sql', DATABASE_NAME, PREFIX + '_')
  db.commit()

  authors = [(FILES[i].get('Author', '').strip(), FILES[i].get('Email', '').lower().strip()) for i in FILES]
  auth = u"INSERT INTO {0}_authors (name, email) VALUES(%s, %s);".format(PREFIX)
  cursor.executemany(auth, set(authors))
  db.commit()

  # Authors
  auth = u"SELECT * FROM {0}_authors;".format(PREFIX)
  cursor.execute(auth)
  db_authors = cursor.fetchall()

  # Stories and bookmarks
  print args

  stories = [(i,
              FILES[i].get('Title', '').replace("'", "\\'"),
              FILES[i].get('Summary', '').replace("'", "\\'"),
              FILES[i].get('Category', '').replace("'", "\\'"),
              FILES[i].get('Characters', '').replace("'", "\\'"),
              datetime.datetime.strptime(
                FILES[i].get('PrintTime',
                             FILES[i].get('DatePrint',
                                          str(datetime.datetime.now().strftime('%m/%d/%y')))),
                '%m/%d/%y').strftime('%Y-%m-%d'),
              FILES[i].get('Location', '').replace("'", "\\'"),
              FILES[i].get('LocationURL', FILES[i].get('StoryURL', '')).replace("'", "\\'"),
              FILES[i].get('Notes', '').replace("'", "\\'"),
              FILES[i].get('Pairing', '').replace("'", "\\'"),  # might be Pairings in some cases
              FILES[i].get('Rating', ''),
              FILES[i].get('Warnings', '').replace("'", "\\'"),
              FILES[i].get('Author', '').strip(),
              FILES[i].get('Email', '').lower().strip(),
              FILES[i].get('FileType', 'bookmark') if _has_file_type(FILES[i]) else args.chapters_file_extensions,
              FILES[i].get('CatOther', '') if FILES[i].get('Category', '') == 'Crossover' else '',
              )
             for i in FILES]

  cur = 0
  total = len(FILES)
  for (original_id, title, summary, category, characters, date, location, url, notes, pairings, rating, warnings, author,
       email, filetype, fandoms) in set(stories):

    cur = Common.print_progress(cur, total)
    try:
      # For AA archives with external links:
      if filetype != 'bookmark':
        filename = location + '.' + filetype
        table_name = '{0}_stories'.format(PREFIX)
      else:
        filename = url
        table_name = '{0}_bookmarks'.format(PREFIX)

      if location == '8/howmany': print filename

      final_fandoms = args.default_fandom if fandoms == '' \
        else  args.default_fandom + ', ' + unicode(fandoms.replace("'", r"\'"), 'utf-8')

      result = [element for element in db_authors if element[1] == author and element[2] == email]
      authorid = result[0][0]

      stor = u"""
        INSERT INTO {0} (id, fandoms, title, summary, tags, characters, date, url, notes, relationships, rating, warnings, authorid)
        VALUES({1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}');\n""" \
        .format(unicode(table_name),
                original_id,
                final_fandoms,
                unicode(title, 'utf-8'),
                unicode(summary, 'utf-8'),
                category,
                characters,
                date,
                filename,
                unicode(notes, 'utf-8'),
                pairings,
                rating,
                warnings,
                authorid)
      cursor.execute(stor)
    except:
      print(title, summary, category, characters, date, location, url)
      raise
  db.commit()


def clean_and_load_data(args):
  data = _clean_file(args.db_input_file)
  _create_mysql(args, data)


def story_to_final_without_tags(story):
  final_story = {
    'id':            story['id'],
    'title':         story['title'],
    'summary ':      story['summary'],
    'notes':         story['notes'],
    'authorid':      story['authorId'],
    'date':          story['date'],
    'updated':       story['updated'],
    'url':           story['url'],
    'ao3url':        story['ao3url'],
    'coauthorid':    story['coauthorId'],
    'imported':      0,
    'doNotImport':   0,
  }
  return final_story


def dummy_chapters(stories):
  return [_dummy_chapter(story) for story in stories]


def _dummy_chapter(story):
  final_chapter = {
    'id':       story['id'],
    'position': 1,
    'title':    story['title'],
    'authorid': story['authorid'],
    'text':     '',
    'date':     story['date'],
    'storyid':  story['id'],
    'notes':    story['notes'],
    'url':      story['url']
  }
  return final_chapter


if __name__ == "__main__":
  args = Args.process_args()
  data = _clean_file(args.filepath)

