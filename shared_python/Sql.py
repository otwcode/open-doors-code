from HTMLParser import HTMLParser
import re

import MySQLdb
import sys


class Sql(object):

  def __init__(self, args):
    self.tag_count = 0
    db = MySQLdb.connect(args.db_host, args.db_user, args.db_password)
    cursor = db.cursor()
    from warnings import filterwarnings
    filterwarnings('ignore', category = MySQLdb.Warning)
    cursor.execute('CREATE DATABASE IF NOT EXISTS {0}'.format(args.temp_db_database))

    self.db = MySQLdb.connect(args.db_host, args.db_user, args.db_password, args.temp_db_database, charset='utf8',
                              use_unicode=True)
    self.cursor = self.db.cursor()
    self.database = args.temp_db_database


  def execute(self, script, parameters = ()):
    self.cursor.execute(script, parameters)
    return self.cursor.fetchall()


  def execute_dict(self, script, parameters = ()):
    dict_cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    dict_cursor.execute(script, parameters)
    return dict_cursor.fetchall()


  def run_script_from_file(self, filename, database, prefix):
    # Open and read the file as a single buffer
    self.cursor.execute('USE {0}'.format(database))
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.replace('$DATABASE$', database).replace('$PREFIX$', prefix).split(';\n')

    # Execute every command from the input file
    for command in sqlCommands:
      # This will skip and report errors
      # For example, if the tables do not yet exist, this will skip over
      # the DROP TABLE commands
      try:
        self.cursor.execute(command)
      except MySQLdb.OperationalError, msg:
        print "Command skipped: ", msg

    self.db.commit()


  def col_exists(self, col, table, database):
    self.cursor.execute("""
        SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{0}' AND TABLE_NAME = '{1}' AND COLUMN_NAME = '{2}'
      """.format(database, table, col))
    result = self.cursor.fetchone()
    return not(result is None)
