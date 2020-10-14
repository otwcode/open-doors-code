class PopulateTags(object):
  def __init__(self, args, db, log, tags, final):
    self.args = args
    self.db = db
    self.database = args.temp_db_database
    self.log = log
    self.tags = tags
    self.final = final

  @staticmethod
  def valid_tags(key, tag_type_list):
    return [d[key].strip() for d in tag_type_list
            if key in d
            and d[key] is not None
            and d[key] != '']

  def tags_for_story(self, story_id, tags_by_type):
    story_tags = {'categories': '', 'fandoms': ''}
    categories = []
    fandoms = []
    for (tag_type, tag_type_tags) in tags_by_type.items():
      if tag_type is None or tag_type == '':
        self.log.warn("\nStory {2} has a None tag type\n {0} -> {1}".format(tag_type, tag_type_tags, story_id))
      else:
        tag_list = [d['ao3_tag'] for d in tag_type_tags if 'ao3_tag' in d and d['ao3_tag'] is not None]
        categories += self.valid_tags('ao3_tag_category', tag_type_tags)
        if tag_type == 'fandoms':
          fandoms += tag_list
        story_tags[tag_type] = ', '.join(set(tag_list))
    if not fandoms:
      fandoms = [self.args.default_fandom]
    story_tags['categories'] = ', '.join(set(categories))
    story_tags['fandoms'] = ', '.join(set(fandoms))
    return story_tags

  def write_tags_for_story(self, tags_by_story_id):
    for (story_id, story_tags) in tags_by_story_id.items():

      # group tags by type into comma-separated lists
      # generate and run SQL to populate story table
      from collections import defaultdict

      tags_by_type = defaultdict(list)
      for tag in story_tags:
        tags_by_type[tag['ao3_tag_type']].append(tag)

      story_tags = self.tags_for_story(story_id, tags_by_type)

      self.final.populate_story_tags(story_id, 'stories', story_tags)
      self.final.populate_story_tags(story_id, 'story_links', story_tags)

  def populate_tags(self):
    self.log.info("Getting all tags per story...")
    tags_by_story_id = self.tags.tags_by_story_id()
    self.write_tags_for_story(tags_by_story_id)
