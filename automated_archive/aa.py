# -- coding: utf-8 --

import datetime
import codecs
import MySQLdb
import re
from shared_python import Args
from shared_python.Sql import Sql


# Convert the Perl hash into a Python dictionary
def _clean_file(filepath):
  archive_db = codecs.open(filepath, 'r', encoding='utf-8').read()

  step1 = (
    archive_db.replace('%FILES = (\n\n', '{\n"').replace('\n)', '\n}')
      .replace('},\n', '},\n"').replace('\t', '    "')
      .replace(' =>', '":').replace(';', ',')
      .replace(',\n"\n},\n1,', '}')
  )
  # Replace line breaks within fields (followed by a character that isn't a space, tab, digit, } or ")
  step2 = re.sub(r"\n(?=[^ \t\d\}\"])", " ", step1)

  # Edit these to fix dodgy data specific to this archive
  final_replace = step2.replace("0,/2,/25", "01/30/00").replace('    "PrintTime": \'P\',\n', "")
  final_regex = re.sub(r"00,02,\d(.*?)',", "02/26/00',", final_replace)

  return eval(final_regex)

#
def _create_mysql(args, FILES):
  db = MySQLdb.connect(args.db_host, args.db_user, args.db_password, "")
  cursor = db.cursor()
  DATABASE_NAME = args.db_database
  PREFIX = args.db_table_prefix

  # Use the database and empty all the tables
  cursor.execute(u"drop database if exists {0};".format(DATABASE_NAME))
  cursor.execute(u"create database {0};".format(DATABASE_NAME))
  cursor.execute(u"use {0}".format(DATABASE_NAME))

  sql = Sql(args)
  sql.run_script_from_file('miscellaneous/open-doors-table-schema.sql', args)
  db.commit()


  authors = [(FILES[i].get('Author', '').strip(), FILES[i].get('Email', '').lower().strip()) for i in FILES]
  auth = u"INSERT INTO {0}_authors (name, email) VALUES(%s, %s);".format(PREFIX)
  cursor.executemany(auth, set(authors))
  db.commit()

  auth = u"SELECT * FROM {0}_authors;".format(PREFIX)
  cursor.execute(auth)
  db_authors = cursor.fetchall()

  stories = [(FILES[i].get('Title', '').replace("'", "\\'"),
              FILES[i].get('Summary', '').replace("'", "\\'"),
              FILES[i].get('Category', '').replace("'", "\\'"),
              FILES[i].get('Characters', '').replace("'", "\\'"),
              datetime.datetime.strptime(FILES[i].get('PrintTime', str(datetime.datetime.now().strftime('%m/%d/%y'))),
                                         '%m/%d/%y')
              .strftime('%Y-%m-%d'),
              # Some AA archives have a filetype
              # FILES[i].get('FileType', 'bookmark'),
              FILES[i].get('Location', '').replace("'", "\\'"),
              FILES[i].get('StoryURL', '').replace("'", "\\'"),
              FILES[i].get('Notes', '').replace("'", "\\'"),
              FILES[i].get('Pairing', '').replace("'", "\\'"),  # might be Pairings in some cases
              FILES[i].get('Rating', ''),
              FILES[i].get('Warnings', '').replace("'", "\\'"),
              FILES[i].get('Author', '').strip(),
              FILES[i].get('Email', '').lower().strip(),
              )
             for i in FILES]
  for (
  title, summary, category, characters, date, location, url, notes, pairings, rating, warnings, author, email) in set(
      stories):
    try:
      table_name = '{0}_stories'.format(PREFIX)
      filename = location + '.html'  # not true for all AA archives!

      # For AA archives with external links:
      # if (filetype != 'bookmark'):
      #   filename = location + '.' + filetype
      #   table_name = '{0}_stories'.format(PREFIX)
      # else:
      #   filename = url
      #   table_name = '{0}_bookmarks'.format(PREFIX)

      result = [element for element in db_authors if element[1] == author and element[2] == email]
      authorid = result[0][0]

      stor = u"""INSERT INTO {0} (fandoms, title, summary, tags, characters, date, url, notes, relationships, rating, warnings, authorid)
      			 VALUES('due South', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}');\n""" \
        .format(unicode(table_name),
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
  data = _clean_file(args.input_file)
  _create_mysql(args, data)


if __name__ == "__main__":
  args = Args.process_args()
  data = _clean_file(args.filepath)

