from html.parser import HTMLParser
import re
import sys
from pymysql import cursors, OperationalError

from shared_python import Common, Logging


class Tags(object):

  def __init__(self, args, db, log):
    self.tag_count = 0
    self.db = db
    self.cursor = self.db.cursor()
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
    try:
      database = self.database if database is None else database
      self.cursor.execute("DROP TABLE IF EXISTS {0}.`tags`".format(database))
    except OperationalError as e:
      self.log.info("Command skipped: {}".format(e))
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS {0}.`tags` (
        `id` int(11) AUTO_INCREMENT,
        `original_tagid` int(11) DEFAULT NULL,
        `original_tag` varchar(1024) DEFAULT NULL,
        `original_parent` varchar(255) DEFAULT NULL,
        `original_table` varchar(255) DEFAULT NULL,
        `original_description` varchar(255) DEFAULT NULL,
        `ao3_tag` varchar(1024) DEFAULT NULL,
        `ao3_tag_type` VARCHAR(255) DEFAULT NULL,
        `ao3_tag_category` VARCHAR(255) DEFAULT NULL,
        `ao3_tag_fandom` VARCHAR(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """.format(database))


  def populate_tag_table(self, database_name, story_id_col_name, table_name, tag_col_lookup, tags_with_fandoms, truncate = True):
    dict_cursor = self.db.cursor(cursors.DictCursor)
    dict_cursor.execute('USE {0}'.format(database_name))
    if truncate:
      dict_cursor.execute('TRUNCATE {0}.`tags`'.format(database_name))

    tag_columns = tag_col_lookup.keys() # [d['col'] for d in tag_col_lookup if 'col' in d]

    # Get all values from all tag columns in the stories table and load as denormalised values in `tags` table
    dict_cursor.execute('SELECT {0}, {1} FROM {2}'.format(story_id_col_name, ', '.join(tag_columns), table_name))
    data = dict_cursor.fetchall()

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
          self.cursor.execute("""
               INSERT INTO tags (storyid, original_tag, original_table, ao3_tag_fandom) VALUES {0}
             """.format(', '.join(values)))

    self.db.commit()


  def distinct_tags(self):
    self.cursor.execute("""
      SELECT DISTINCT
        id as "Original Tag ID",
        original_tag as "Original Tag Name",
        original_parent as "Original Parent Tag",
        ao3_tag_fandom as "Related Fandom",
        ao3_tag as "Recommended AO3 Tag",
        ao3_tag_type as "Recommended AO3 Type",
        ao3_tag_category as "Recommended AO3 Category",
        original_description as "Original Description",
        '' as "TW Notes" FROM tags
      """)
    return self.cursor.fetchall()


  def update_tag_row(self, row):
    tag_headers = self.tag_export_map
    tag = str(row[tag_headers['original_tag']]).replace("'", r"\'")
    tag_id = row[tag_headers['id']]

    if tag_id == '' or tag_id is None:
      tagid_filter = f"original_tag = '{tag}'"
    else:
      tagid_filter = f"id={tag_id}"

    fandom = row[tag_headers['ao3_tag_fandom']].replace("'", r"\'")
    ao3_tags = row[tag_headers['ao3_tag']].replace("'", r"\'").split(",")
    ao3_tag_types = row[tag_headers['ao3_tag_type']].split(",")
    number_types = len(ao3_tag_types)

    # If tags length > types length -> there are remapped tags
    # Iterate over all the provided AO3 tags:
    # - First tag -> update the existing row
    # - Other tags -> create new row in tags table
    for idx, ao3_tag in enumerate(ao3_tags):
      if number_types >= idx + 1:
        ao3_tag_type = ao3_tag_types[idx].strip()
      else:
        ao3_tag_type = ao3_tag_types[0].strip()

      self.cursor.execute(f"USE {self.database}")

      if idx > 0:
        self.cursor.execute(f"""
          INSERT INTO tags (ao3_tag, ao3_tag_type, ao3_tag_category, ao3_tag_fandom, 
          original_tag, original_tagid)
          VALUES ('{ao3_tag}', '{ao3_tag_type}', '{row[tag_headers['ao3_tag_category']]}', 
          '{fandom}', '{tag}', '{tag_id}')
        """)
        # FIXME OD-574 need to also insert entries in item_tags for the new tags
      else:
        self.cursor.execute(f"""
              UPDATE tags
              SET ao3_tag='{str(ao3_tag)}', ao3_tag_type='{ao3_tag_type}', 
              ao3_tag_category='{row[tag_headers['ao3_tag_category']]}', 
              ao3_tag_fandom='{fandom}'
              WHERE {tagid_filter}
            """)
      self.db.commit()

  def tags_by_story_id(self):
    self.cursor.execute("SELECT DISTINCT storyid FROM tags;")
    storyids = self.cursor.fetchall()
    cur = 0
    total = len(storyids)

    dict_cursor = self.db.cursor(cursors.DictCursor)
    tags_by_story_id = {}
    for storyid in storyids:
      cur += 1
      sys.stdout.write('\rCollecting tags for {0}/{1} stories and bookmarks (including DNI)'.format(cur, total))
      sys.stdout.flush()

      dict_cursor.execute("SELECT * FROM tags WHERE storyid={0}".format(storyid[0]))
      tags = dict_cursor.fetchall()
      tags_by_story_id[storyid[0]] = tags
    return tags_by_story_id
