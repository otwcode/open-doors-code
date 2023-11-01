import re

from shared_python.Args import Args
from shared_python.Sql import Sql
from shared_python.Tags import Tags


if __name__ == "__main__":
  """
  Only for non-eFiction archives.
  This script creates a table called tags in the temporary database and denormalises all the tags for each story.
  This table is the basis for the Tag Wrangling sheet and is used to map the tags back to the story when the final
  tables are created.
  """
  args_obj = Args()
  args = args_obj.args_for_02()
  log = args_obj.logger_with_filename()
  sql = Sql(args, log)
  tags = Tags(args, sql, log)
  log.info('Processing tags from stories and bookmarks table in {0}'.format(args.temp_db_database))
  tags.create_tags_table()

  tag_col_list = {}
  stories_id_name = ""
  stories_table_name = ""

  # AUTOMATED ARCHIVE
  if args.archive_type == 'AA':

    story_table_name = input('Story table name (default: "stories"): ')
    if story_table_name is None or story_table_name == '':
      story_table_name = 'stories'

    bookmark_table_name = input('Bookmark table name (default: "story_links"): ')
    if bookmark_table_name is None or bookmark_table_name == '':
      bookmark_table_name = 'story_links'

    tag_columns = input('Column names containing tags \n   (delimited by commas - default: "rating, tags, warnings, characters, fandoms, relationships"): ')
    if tag_columns is None or tag_columns == '':
      tag_columns = "rating, tags, warnings, characters, fandoms, relationships"
    # fancy footwork to ensure compatibility with eFiction
    tag_col_list = re.split(r", ?", tag_columns)
    tag_columns_dict = dict(zip(tag_col_list, tag_col_list))
    fields_with_fandom = args.fields_with_fandom.split(", ") if args.fields_with_fandom is not None else []
    tags.populate_tag_table(args.temp_db_database, "id", story_table_name, tag_columns_dict, fields_with_fandom)
    tags.populate_tag_table(args.temp_db_database, "id", bookmark_table_name, tag_columns_dict, fields_with_fandom, False)

  log.info("Done extracting tags.")
