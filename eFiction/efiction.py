import os
import re

from shared_python.FinalTables import FinalTables


class eFiction(object):

  def __init__(self, args, sql, log, tags):
    self.args = args
    self.sql = sql
    self.db = sql.db
    self.cursor = self.db.cursor()
    self.log = log
    self.efiction_original_database = self.load_database()
    self.tags = tags

  @staticmethod
  def column_schema(column_name):
    col_to_table = {
      'catid': {
        'col': 'catid',
        'table_name': 'fanfiction_categories',
        'field_name': 'category',
        'id_name': 'catid',
        'lookup_field': 'parentcatid',
        'lookup_table': 'fanfiction_categories',
        'lookup_table_field': 'category',
        'lookup_id': 'catid',
        'extra_column': 'description'
      },
      'classes': {
        'col': 'classes',
        'table_name': 'fanfiction_classes',
        'field_name': 'class_name',
        'id_name': 'class_id',
        'lookup_field': 'class_type',
        'lookup_table': 'fanfiction_classtypes',
        'lookup_table_field': 'classtype_title',
        'lookup_id': 'classtype_id'
      },
      'charid': {
        'col': 'charid',
        'table_name': 'fanfiction_characters',  # has catid
        'field_name': 'charname',
        'id_name': 'charid',
        'lookup_field': 'catid',
        'lookup_table': 'fanfiction_categories',
        'lookup_table_field': 'category',
        'lookup_id': 'catid'
      },
      'rid': {
        'col': 'rid',
        'table_name': 'fanfiction_ratings',
        'field_name': 'rating',
        'id_name': 'rid'
      },
      'gid': {
        'col': 'gid',
        'table_name': 'fanfiction_genres',
        'field_name': 'genre',
        'id_name': 'gid'
      },
      'wid': {
        'col': 'wid',
        'table_name': 'fanfiction_warnings',
        'field_name': 'warning',
        'id_name': 'wid'
      }
    }
    return col_to_table[column_name]

  @staticmethod
  def table_names():
    table_names = {
      'authors': 'fanfiction_authors',
      'stories': 'fanfiction_stories',
      'chapters': 'fanfiction_chapters',
      'bookmarks': None
    }
    return table_names

  @staticmethod
  def author_to_final(efiction_author):
    final_author = {
      'id': efiction_author['uid'],
      'name': efiction_author['penname'],
      'email': efiction_author['email'],
      'imported': 0,
      'do_not_import': 0
    }
    return final_author

  @staticmethod
  def story_to_final_without_tags(efiction_story):
    final_story = {
      'id': efiction_story['sid'],
      'title': efiction_story['title'],
      'summary ': efiction_story['summary'],
      'notes': efiction_story.get('storynotes', ''),
      'author_id': efiction_story['uid'],
      'coauthor_id': efiction_story['coauthors'],
      'date': efiction_story['date'],
      'updated': efiction_story['updated'],
      'imported': 0,
      'do_not_import': 0,
      # Not in eFiction original table
      # 'url':           efiction_story['url'],
      # 'ao3url':        efiction_story['ao3url'],
      # 'coauthorid':    efiction_story['coauthorid'],
      # 'tags':          efiction_story['tags'],
      # 'rating':        efiction_story['rating'],
      # 'fandoms':       efiction_story['fandoms'],
      # 'warnings':      efiction_story['warnings'],
      # 'categories':    efiction_story['categories'],
      # 'characters':    efiction_story['characters'],
      # 'relationships': efiction_story['characters']
    }
    return final_story

  @staticmethod
  def chapter_to_final(efiction_chapter):
    final_chapter = {
      'ID': efiction_chapter['chapid'],
      'Position': efiction_chapter['inorder'],
      'Title': efiction_chapter['title'],
      'author_id': efiction_chapter['uid'],
      'Text': efiction_chapter['storytext'],
      'Date': None,
      'story_id': efiction_chapter['sid'],
      'Notes': efiction_chapter['notes'],
      'Url': None
      # efiction_chapter['endnotes'],
    }
    return final_chapter

  @staticmethod
  def add_coauthors_to_stories(db, stories):
    for story in stories:
      db.cursor.execute("SELECT * FROM fanfiction_coauthors WHERE sid=%i", story['sid'])
    return None

  def load_database(self):
    original_database = "{}_efiction".format(self.args.temp_db_database)
    self.log.info('Loading eFiction file "{0}" into database "{1}"'.format(self.args.db_input_file, original_database))
    self.sql.run_script_from_file(self.args.db_input_file,
                                  database=original_database,
                                  initial_load=True)
    return original_database

  def copy_tags_to_tags_table(self, default_tag_columns="", default_has_ids_in_tags=""):
    # Extract tags
    self.log.info(
      'Processing tags from stories and bookmarks table in {0} to {1}.tags'.format(self.efiction_original_database,
                                                                                   self.args.temp_db_database))
    self.tags.create_tags_table(self.efiction_original_database)
    tag_col_list = {}
    if default_tag_columns == '':
      tag_columns = raw_input(
        'Column names containing tags \n     (delimited by commas - default: "catid, classes, charid, rid, gid, wid"): ')
    else:
      tag_columns = default_tag_columns
    if tag_columns is None or tag_columns == '':
      tag_columns = "catid, classessql, charid, rid, gid, wid"
    for col in re.split(r", ?", tag_columns):
      if self.sql.col_exists(col, "fanfiction_stories", self.efiction_original_database):
        tag_col_list[col] = self.column_schema(col)
    self.tags.populate_tag_table(self.efiction_original_database, "sid", "fanfiction_stories", tag_col_list, '')

    if default_has_ids_in_tags == "":
      has_ids_in_tags = raw_input('Do all the tag fields contain ids? (y, n) ')
    else:
      has_ids_in_tags = default_has_ids_in_tags
    for col in tag_col_list.keys():
      self.log.debug("\nProcessing {0}".format(col))
      table = self.column_schema(col)
      self.tags.hydrate_tags_table(col, table, has_ids_in_tags == 'y')

  def copy_to_temp_db(self, has_coauthors=None):
    efiction_db = self.efiction_original_database
    temp_db = self.args.temp_db_database
    coauthors = {}
    table_names = self.table_names()
    if has_coauthors is None:
      has_coauthor_table = raw_input("\nDoes this archive have a coauthors table? Y/N\n")
      has_coauthors = True if str.lower(has_coauthor_table) == 'y' else False
    else:
      has_coauthors = has_coauthors
    if has_coauthors:
      coauthors_dict = self.sql.execute_dict("SELECT * FROM fanfiction_coauthors")
      for coauthor in coauthors_dict:
        coauthors[coauthor['sid']] = coauthor['uid']

    # Create Open Doors tables in temp db
    self.sql.run_script_from_file(
      os.path.join(os.path.dirname(__file__), '../shared_python/create-open-doors-tables.sql'),
      database=temp_db)

    # Export data to Open Doors tables
    final = FinalTables(self.args, self.sql.db, self.log)
    stories_without_tags = final.original_table(table_names['stories'], database_name=efiction_db)
    self.log.info("Stories without tags in original eFiction: {0}".format(len(stories_without_tags)))
    chapters = final.original_table(table_names['chapters'], database_name=efiction_db)
    self.log.info("Chapters in original eFiction: {0}".format(len(chapters)))

    # STORIES
    self.log.info("Copying stories to temporary table {0}.stories...".format(temp_db))
    final_stories = []
    for story in stories_without_tags:
      if coauthors is not None and coauthors.has_key(story['sid']):
        story['coauthors'] = coauthors[story['sid']]
      else:
        story['coauthors'] = None
      final_stories.append(self.story_to_final_without_tags(story))
    final.insert_into_final('stories', final_stories, temp_db)

    # AUTHORS
    self.log.info("Copying authors from original eFiction source...")
    final_authors = []
    authors = final.original_table(table_names['authors'], database_name=self.efiction_original_database)
    for author in authors:
      final_author = self.author_to_final(author)
      final_authors.append(final_author)
    final.insert_into_final('authors', final_authors, temp_db)

    # CHAPTERS
    self.log.info("Copying chapters from original eFiction source...")
    final_chapters = [self.chapter_to_final(chapter) for chapter in chapters]
    final.insert_into_final('chapters', final_chapters, temp_db)

    # TAGS
    self.log.info("Copying tags from original eFiction source...")
    final_tags = final.original_table('tags', database_name=self.efiction_original_database)
    self.tags.create_tags_table(temp_db)
    final.insert_into_final('tags', final_tags, temp_db)


  def convert_efiction_to_temp(self):
    self.copy_tags_to_tags_table()
    self.copy_to_temp_db()
