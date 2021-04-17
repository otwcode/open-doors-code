import datetime
import html
from logging import Logger

from pymysql import cursors


class FinalTables(object):

    def __init__(self, args, db, log: Logger):
        self.args = args
        self.db = db
        self.dict_cursor = self.db.cursor(cursors.DictCursor)
        self.original_database = args.temp_db_database
        self.final_database = args.output_database
        self.log = log

    def original_table(self, table_name, filter='', database_name=None):
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
        return html.unescape(item).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")

    def _value(self, row):
        value = []
        for item in row:
            if type(item) is str:
                value.append('"' + self._escape_unescape(item) + '"')
            elif type(item) is datetime.datetime:
                value.append('"' + str(item) + '"')
            elif item is None:
                value.append('null')
            elif item == '':
                value.append('""')
            else:
                value.append(str(item))
        return value

    def insert_into_final(self, output_table_name, rows, target_database=None):
        if target_database:
            final_database = target_database
        else:
            final_database = self.final_database
        self.dict_cursor.execute("TRUNCATE `{0}`.`{1}`".format(final_database, output_table_name))
        columns = rows[0].keys()
        values = []
        for row in rows:
            col = self._value(row.values())
            values.append('(' + ', '.join(col) + ')')

        self.dict_cursor.execute(f"""
            INSERT INTO `{final_database}`.`{output_table_name}` ({', '.join(columns)}) VALUES {', '.join(values)}
          """)
        self.db.commit()

    def populate_story_tags(self, story_id, output_table_name, story_tags):
        cols_with_tags = []
        for (col, tags) in story_tags.items():
            cols_with_tags.append(u"{0}='{1}'".format(col, tags.replace("'", "\\'").strip()))

        if cols_with_tags:
            self.dict_cursor.execute("""
         UPDATE `{0}`.`{1}` SET {2} WHERE id={3}
        """.format(self.final_database, output_table_name, ", ".join(cols_with_tags), story_id))
            self.db.commit()

    def story_to_final_without_tags(self, story, story_authors, is_story=True):
        type = 'story' if is_story else 'story_link'
        authors_count = len(story_authors)
        notes = story['notes']
        if authors_count > 2:
            # AO3 works can't currently be imported with more than two authors
            self.log.warning(f"{type} {story['id']} has {authors_count} authors - listing all authors in notes...")
            author_names = "Creators: {} and {}".format(", ".join(story_authors[:-1]),  story_authors[-1])
            notes = "{author_names}<br/><br/>{notes}" if notes else author_names

        final_story = {
            'id': story['id'],
            'title': story['title'],
            'summary ': story['summary'],
            'notes': notes,
            'author_id': story_authors[0]["author_id"],
            'date': story['date'],
            'updated': story['updated'],
            'url': story['url'],
            'ao3_url': story['ao3_url'],
            'imported': 0,
            'do_not_import': 0,
        }
        if is_story:
            # AO3 bookmarks can't currently be imported with multiple authors, so only populate the coauthor for works
            final_story['coauthor_id'] = story_authors[1]["author_id"] if authors_count > 1 else None
        return final_story

    def dummy_chapters(self, stories):
        return [self._dummy_chapter(story) for story in stories]

    def _dummy_chapter(self, story):
        chapter = {k.lower(): v for k, v in story.iteritems()}
        final_chapter = {
            'id': chapter['id'],
            'position': chapter.get('position', 1),
            'title': chapter['title'],
            'text': chapter.get('text', ''),
            'date': chapter['date'],
            'story_id': chapter['id'],
            'notes': chapter['notes'],
            'url': chapter['url']
        }
        return final_chapter
