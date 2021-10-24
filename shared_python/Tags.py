import re
from html.parser import HTMLParser
from logging import Logger

import sys
from pymysql import cursors, OperationalError

from shared_python.Sql import Sql

class Tags(object):

  def __init__(self, args, sql: Sql, log: Logger):
    self.tag_count = 0
    self.sql = sql
    self.database = args.temp_db_database
    self.html_parser = HTMLParser()
    self.log = log

    self.tag_export_map = {
      'id':                   'Original Tag ID',
      'original_tag':         'Original Tag',
      'original_parent':      'Original Parent Tag',
      'original_table':       'Original Tag Type',
      'original_description': 'Original Tag Description',
      'ao3_tag':              'Recommended AO3 Tag',
      'ao3_tag_category':     'Recommended AO3 Category (for relationships)',
      'ao3_tag_type':         'Recommended AO3 Type',
      'ao3_tag_fandom':       'Related Fandom'
    }


  def create_tags_table(self, database = None):
    """
    Used only in step 02 for non-eFiction archives
    """
    try:
      database = self.database if database is None else database
      self.sql.execute("DROP TABLE IF EXISTS {0}.`tags`".format(database))
    except OperationalError as e:
      self.log.info("Command skipped: {}".format(e))
    self.sql.execute("""
      CREATE TABLE IF NOT EXISTS {0}.`tags` (
        `id` int(11) AUTO_INCREMENT,
        `original_tagid` int(11) DEFAULT NULL,
        `original_tag` varchar(1024) DEFAULT NULL,
        `original_parent` varchar(255) DEFAULT NULL,
        `original_table` varchar(255) DEFAULT NULL,
        `original_description` text DEFAULT NULL,
        `ao3_tag` varchar(1024) DEFAULT NULL,
        `ao3_tag_type` VARCHAR(255) DEFAULT NULL,
        `ao3_tag_category` VARCHAR(255) DEFAULT NULL,
        `ao3_tag_fandom` VARCHAR(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """.format(database))


  def populate_tag_table(self, database_name, story_id_col_name, table_name, tag_col_lookup, tags_with_fandoms, truncate = True):
    """
    Used only in step 02 for non-eFiction archives
    """
    self.sql.execute('USE {0}'.format(database_name))
    if truncate:
      self.sql.execute('TRUNCATE {0}.`tags`'.format(database_name))

    tag_columns = tag_col_lookup.keys() # [d['col'] for d in tag_col_lookup if 'col' in d]

    # Get all values from all tag columns in the stories table and load as denormalised values in `tags` table
    data = self.sql.execute_dict('SELECT {0}, {1} FROM {2}'.format(story_id_col_name, ', '.join(tag_columns), table_name))

    for story_tags_row in data :
      values = []
      for col in tag_columns:
        needs_fandom = col in tags_with_fandoms
        if story_tags_row[col] is not None:
          for val in re.split(r", ?", story_tags_row[col]):
            if val != '':
              if type(tag_col_lookup[col]) is str: # Probably AA or a custom archive
                cleaned_tag = val.encode('utf-8').replace("'", "\'").strip()

                values.append('({0}, "{1}", "{2}", "{3}")'
                              .format(story_tags_row[story_id_col_name],
                                      re.sub(r'(?<!\\)"', '\\"', cleaned_tag),
                                      tag_col_lookup[col],
                                      story_tags_row['fandoms'] if needs_fandom else ''))

      if len(values) > 0:
          self.sql.execute("""
               INSERT INTO tags (storyid, original_tag, original_table, ao3_tag_fandom) VALUES {0}
             """.format(', '.join(values)))


  def distinct_tags(self, database):
    """
    Used in step 03. Maps table columns to the names used in the Tag Wrangling sheet.
    :return: distinct rows from the tags table with renamed columns
    """
    return self.sql.execute_and_fetchall(database, """
      SELECT DISTINCT
        id as "Original Tag ID",
        original_tag as "Original Tag Name",
        original_type as "Original Tag Type",
        original_parent as "Original Parent Tag",
        ao3_tag_fandom as "Related Fandom",
        ao3_tag as "Recommended AO3 Tag",
        ao3_tag_type as "Recommended AO3 Type",
        ao3_tag_category as "Recommended AO3 Category",
        original_description as "Original Description",
        '' as "TW Notes" FROM tags
      """)


  def update_tag_row(self, row: dict):
    """
    Used in step 04.
    :param row: a row from the Tag Wrangling spreadsheet as a dict
    :return: number of newly inserted rows to item_tags
    """
    tag_headers = self.tag_export_map
    tag = str(row[tag_headers['original_tag']]).replace("'", r"\'")
    tag_id = row[tag_headers['id']]

    if tag_id == '' or tag_id is None or not tag_id.isnumeric():
      tagid_filter = f"original_tag = '{tag}'"
    else:
      tagid_filter = f"id={tag_id}"

    fandom = row[tag_headers['ao3_tag_fandom']].replace("'", r"\'")
    ao3_tags = row[tag_headers['ao3_tag']].replace("'", r"\'").split(",")
    ao3_tag_types = row[tag_headers['ao3_tag_type']].split(",")
    number_types = len(ao3_tag_types)

    num_insert = 0
    # If tags length > types length -> there are remapped tags
    # Iterate over all the provided AO3 tags:
    # - First tag -> update the existing row
    # - Other tags -> create new row in tags table
    for idx, ao3_tag in enumerate(ao3_tags):
      ao3_tag = ao3_tag.lstrip().rstrip()
      if number_types >= idx + 1:
        ao3_tag_type = ao3_tag_types[idx].strip()
      else:
        ao3_tag_type = ao3_tag_types[0].strip()

      self.sql.execute(f"USE {self.database}")

      if idx > 0:
        self.sql.execute(f"""
          INSERT INTO tags (ao3_tag, ao3_tag_type, ao3_tag_category, ao3_tag_fandom, 
          original_tag, original_tagid)
          VALUES ('{ao3_tag}', '{ao3_tag_type}', '{row[tag_headers['ao3_tag_category']]}', 
          '{fandom}', '{tag}', '{tag_id}')
        """)
        # get last auto increment tag id
        sql_dict = self.sql.execute_dict(f"""select LAST_INSERT_ID();""")
        new_tag_id = sql_dict[0]['LAST_INSERT_ID()']
        # get all associated items from item_tags
        items = self.sql.execute_dict(f"""SELECT item_id, item_type 
                                          FROM item_tags WHERE tag_id = {row['Original Tag ID']}""")
        
        # insert into item_tags table
        for item in items:
          item_id, item_type = item['item_id'], item['item_type']
          self.sql.execute(f"""INSERT INTO item_tags (item_id, item_type, tag_id) VALUES ('{item_id}', '{item_type}', '{new_tag_id}')""")
          num_insert += 1
      else:
        self.sql.execute(f"""
              UPDATE tags
              SET ao3_tag='{str(ao3_tag)}', ao3_tag_type='{ao3_tag_type}', 
              ao3_tag_category='{row[tag_headers['ao3_tag_category']]}', 
              ao3_tag_fandom='{fandom}'
              WHERE {tagid_filter}
            """)
    return num_insert

  def tags_by_story_id(self, item_type: str = 'story'):
    story_ids = \
      self.sql.execute_and_fetchall(self.database,
                                    f"""
                                    SELECT item_id, item_type, GROUP_CONCAT(tag_id) as tag_ids
                                    FROM item_tags WHERE item_type='{item_type}' GROUP BY item_id, item_type ;""")
    cur = 0
    total = len(story_ids)

    tags_by_story_id = {}
    for story_id in story_ids:
      cur += 1
      sys.stdout.write(f'\rCollecting tags for {item_type}: {cur}/{total}  (including Do Not Import)')
      sys.stdout.flush()
      tags = self.sql.execute_dict(f"SELECT * FROM tags WHERE id in ({story_id[2]})")
      tags_by_story_id[story_id[0]] = tags
    return tags_by_story_id
