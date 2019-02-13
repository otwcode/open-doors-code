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
      'table_name': 'fanfiction_characters', # has catid
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


def table_names():
  table_names = {
    'authors': 'fanfiction_authors',
    'stories': 'fanfiction_stories',
    'chapters': 'fanfiction_chapters',
    'bookmarks': None
  }
  return table_names

def author_to_final(efiction_author):
  final_author = {
    'id':            efiction_author['uid'],
    'name':          efiction_author['penname'],
    'email':         efiction_author['email'],
    'imported':      0,
    'do_not_import': 0
  }
  return final_author


def story_to_final_without_tags(efiction_story):
  final_story = {
    'id':            efiction_story['sid'],
    'title':         efiction_story['title'],
    'summary ':      efiction_story['summary'],
    'notes':         efiction_story.get('storynotes', ''),
    'author_id':     efiction_story['uid'],
    'coauthor_id':   efiction_story['coauthors'],
    'date':          efiction_story['date'],
    'updated':       efiction_story['updated'],
    'imported':      0,
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


def chapter_to_final(efiction_chapter):
  final_chapter = {
    'ID':        efiction_chapter['chapid'],
    'Position':  efiction_chapter['inorder'],
    'Title':     efiction_chapter['title'],
    'author_id': efiction_chapter['uid'],
    'Text':      efiction_chapter['storytext'],
    'Date':      None,
    'story_id':  efiction_chapter['sid'],
    'Notes':     efiction_chapter['notes'],
    'Url':       None
    # efiction_chapter['endnotes'],
  }
  return final_chapter

def add_coauthors_to_stories(db, stories):
  for story in stories:
    db.cursor.execute("SELECT * FROM fanfiction_coauthors WHERE sid=%i", story['sid'])
  return None
