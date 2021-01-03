from html.parser import HTMLParser

import MySQLdb
import datetime


class FinalTables(object):

  def __init__(self, args, db, log):
    self.args = args
    self.db = db
    self.dict_cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    self.original_database = args.temp_db_database
    self.final_database = args.output_database
    self.html_parser = HTMLParser()
    self.log = log


  def original_table(self, table_name, filter = '', database_name = None):
    if table_name is None:
      return None
    if database_name is None:
      original_database = self.original_database
    else:
      original_database = database_name
    query = "SELECT * FROM `{0}`.`{1}` {2}".format(original_database, table_name, filter)
    self.dict_cursor.execute(query)
    return self.dict_cursor.fetchall()


  def _escape_unescape(self, item):
    return self.html_parser.unescape(item).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


  def _value(self, row):
    value = []
    for item in row:
      if type(item) is str:
        value.append('"' + self._escape_unescape(item) + '"')
      elif type(item) is datetime.datetime:
        value.append('"' + str(item) + '"')
      elif item is None:
        value.append('null')
      elif item is '':
        value.append('""')
      else:
        value.append(item)
    return value


  def insert_into_final(self, output_table_name, rows, target_database = None):
    if target_database:
      final_database = target_database
    else:
      final_database = self.final_database
    self.dict_cursor.execute("TRUNCATE `{0}`.`{1}`".format(final_database, output_table_name))
    columns = rows[0].keys()
    values = []
    for row in rows:
      r = self._value(row.values())
      values.append('(' + u', '.join(r) + ')')

    self.dict_cursor.execute(u"""
       INSERT INTO `{0}`.`{1}` ({2})
       VALUES {3}
      """.format(final_database, output_table_name, ', '.join(columns), u', '.join(values)))
    self.db.commit()


  def populate_story_tags(self, story_id, output_table_name, story_tags):
    cols_with_tags = []
    for (col, tags) in story_tags.items():
      cols_with_tags.append(u"{0}='{1}'".format(col, tags.replace("'", "\\'").strip()))

    if cols_with_tags:
      self.dict_cursor.execute(u"""
         UPDATE `{0}`.`{1}` SET {2} WHERE id={3}
        """.format(self.final_database, output_table_name, ", ".join(cols_with_tags), story_id))
      self.db.commit()
