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
        `original_column` varchar(255) DEFAULT NULL,
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

                values.append('({0}, "{1}", "{2}", "{3}", "{4}")'
                              .format(story_tags_row[story_id_col_name],
                                      re.sub(r'(?<!\\)"', '\\"', cleaned_tag),
                                      col,
                                      tag_col_lookup[col],
                                      story_tags_row['fandoms'] if needs_fandom else ''))

      if len(values) > 0:
          self.cursor.execute("""
               INSERT INTO tags (storyid, original_tag, original_column, original_table, ao3_tag_fandom) VALUES {0}
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
          original_tag, original_tagid, original_column)
          VALUES ('{ao3_tag}', '{ao3_tag_type}', '{row[tag_headers['ao3_tag_category']]}', 
          '{fandom}', '{tagid_filter}', {tag}, 
          '{row[tag_headers['original_tagid']] or 'null'}')
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


  def hydrate_tag_row(self, tag_id, tag_to_look_up, tag, col, table, parent ='', description =''):
    self.cursor.execute("""
        UPDATE `tags`
        SET original_tagid=%s, original_tag=%s, original_parent=%s, original_description=%s, original_table=%s
        WHERE original_tag=%s and original_column=%s
      """,
      (tag_id, self.html_parser.unescape(tag.strip()), self.html_parser.unescape(parent.strip()), self.html_parser.unescape(description.strip()), table, tag_to_look_up.strip(), col))
    self.db.commit()


  def hydrate_tags_table(self, col, lookup_data, lookup_ids = False):
    self.cursor.execute('SELECT DISTINCT original_tag from tags WHERE original_column="{0}"'.format(col))
    results = self.cursor.fetchall()
    total = len(results)
    cur = 0
    self.log.info("{0} tags for column '{1}'".format(total, col))

    for tag_row in results:
      cur = Common.print_progress(cur, total)

      # Get tag data
      parent = ''
      extra_column = ', {0} as description'.format(lookup_data['extra_column']) if 'extra_column' in lookup_data else ''
      lookup_column = ', {0} as parent'.format(lookup_data['lookup_field']) if 'lookup_field' in lookup_data else ''
      matching_field = lookup_data['id_name'] if lookup_ids else lookup_data['field_name']

      dict_cursor = self.db.cursor(cursors.DictCursor)
      dict_cursor.execute("""
          SELECT {0}, {1}{2}{3} FROM {4} WHERE {5}='{6}'
        """.format(lookup_data['id_name'], lookup_data['field_name'], lookup_column, extra_column, lookup_data['table_name'], matching_field, tag_row[0]))
      tag = dict_cursor.fetchone()
      if tag is not None:
        # Get parent data
        if 'lookup_field' in lookup_data:
          self.cursor.execute("SELECT {0} FROM {1} WHERE {2}='{3}'"
                            .format(lookup_data['lookup_table_field'],
                                    lookup_data['lookup_table'],
                                    lookup_data['lookup_id'],
                                    tag['parent']))
          result = self.cursor.fetchone()
          parent = result[0] if result is not None else ''

        # Update the table
        description = tag['description'] if 'description' in tag else ''
        self.hydrate_tag_row(tag_id = tag[lookup_data['id_name']],
                            tag_to_look_up= tag_row[0],
                            tag = tag[lookup_data['field_name']],
                            table = lookup_data['table_name'],
                            col = col, parent = parent, description = description)


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
