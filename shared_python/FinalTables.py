from HTMLParser import HTMLParser

import MySQLdb
import datetime


class FinalTables(object):

  def __init__(self, args, db):
    self.args = args
    self.db = db
    self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    self.original_database = args.db_database
    self.final_database = args.output_database
    self.html_parser = HTMLParser()


  def original_table(self, table_name, filter = ''):
    self.cursor.execute("SELECT * FROM `{0}`.`{1}` {2}".format(self.original_database, table_name, filter))
    return self.cursor.fetchall()


  def _escape_unescape(self, item):
    return self.html_parser.unescape(item).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


  def _value(self, row):
    value = []
    for item in row:
      if type(item) is unicode:
        value.append('"' + self._escape_unescape(item) + '"')
      elif type(item) is datetime.datetime:
        value.append('"' + unicode(item) + '"')
      elif item is None:
        value.append('null')
      else:
        value.append(unicode(item))
    return value


  def insert_into_final(self, output_table_name, rows):
    self.cursor.execute("TRUNCATE `{0}`.`{1}`".format(self.final_database, output_table_name))
    columns = rows[0].keys()
    values = []
    for row in rows:
      r = self._value(row.values())
      values.append('(' + u', '.join(r) + ')')

    self.cursor.execute(u"""
       INSERT INTO `{0}`.`{1}` ({2})
       VALUES {3}
      """.format(self.final_database, output_table_name, ', '.join(columns), u', '.join(values)))
    self.db.commit()


  def populate_story_tags(self, story_id, output_table_name, story_tags):
    cols_with_tags = []
    for (col, tags) in story_tags.items():
      cols_with_tags.append(u"{0}='{1}'".format(col, tags.replace("'", "\\'").strip()))

    if cols_with_tags:
      self.cursor.execute(u"""
         UPDATE `{0}`.`{1}` SET {2} WHERE id={3}
        """.format(self.final_database, output_table_name, ", ".join(cols_with_tags), story_id))
      self.db.commit()
