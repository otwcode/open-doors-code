# encoding: utf-8
import os

from shared_python.Args import Args
from shared_python.FinalTables import FinalTables
from shared_python.Sql import Sql


def _clean_email(author):
    """
    Tidy up author emails that might be missing after earlier stages
    :param author: row from the authors table
    :return:
    """
    email = author['email']
    if email is None or email == '':
        email = u'{0}{1}Archive@ao3.org'.format(author['name'], args.archive_name) \
            .replace(' ', '').replace("'", "")
    if email.startswith('mailto:'):
        email = author['email'].replace('mailto:', '')
    return email


def main(args, log):
    sql = Sql(args, log)
    final = FinalTables(args, sql, log)

    log.info("Creating final destination tables in {0}".format(args.output_database))

    table_names = {
        'authors': 'authors',
        'stories': 'stories',
        'chapters': 'chapters',
        'story_links': 'story_links'
    }
    filter = 'WHERE id NOT IN '

    sql.run_script_from_file('shared_python/create-open-doors-tables.sql',
                             database=args.output_database)

    # Filter out DNI stories - story_ids_to_remove must be comma-separated list of DNI ids
    story_exclusion_filter = ''
    if os.path.exists(args.story_ids_to_remove):
        with open(args.story_ids_to_remove, "rt") as f:
            log.info("Removing {0} Do Not Import stories...".format(sum(line.count(",") for line in f) + 1))
            f.seek(0)
            for line in f:
                story_exclusion_filter = filter + '(' + line + ')'

    # Filter out DNI stories - bookmark_ids_to_remove must be comma-separated list of DNI ids
    bookmark_exclusion_filter = ''
    if args.bookmark_ids_to_remove and os.path.exists(args.bookmark_ids_to_remove):
        with open(args.bookmark_ids_to_remove, "rt") as f:
            log.info("Removing {0} Do Not Import bookmarks...".format(sum(line.count(",") for line in f) + 1))
            f.seek(0)
            for line in f:
                bookmark_exclusion_filter = filter + '(' + line + ')'

    # Load filtered tables into variables
    stories_without_tags = final.original_table(table_names['stories'], story_exclusion_filter)
    log.info("Stories without tags after removing DNI: {0}".format(len(stories_without_tags)))
    bookmarks_without_tags = final.original_table(table_names['story_links'], bookmark_exclusion_filter)
    if bookmarks_without_tags:
        log.info("Bookmarks without tags after removing DNI: {0}".format(len(bookmarks_without_tags)))
    else:
        log.info("No bookmarks to remove")

    # STORIES
    log.info("Copying stories to final table {0}.stories...".format(args.output_database))
    final_stories = []
    for story in stories_without_tags:
        story_authors = final.original_table('item_authors', f"WHERE item_id={story['id']} and item_type='story'")
        # Add additional story processing here
        if len(story_authors) > 0:
            final_stories.append(final.story_to_final_without_tags(story, story_authors))
        else: 
            log.warning(f"Story with id {story['id']} has no authors, and will not be imported")
    final.insert_into_final('stories', final_stories)

    # BOOKMARKS
    if bookmarks_without_tags is not None:
        log.info("Copying bookmarks to final table {0}.story_links...".format(args.output_database))
        final_bookmarks = []
        for bookmark in bookmarks_without_tags:
            # Add additional bookmark processing here
            bookmark_authors = final.original_table('item_authors',
                                                    f"WHERE item_id={bookmark['id']} and item_type='story_link'")
            final_bookmarks.append(final.story_to_final_without_tags(bookmark, bookmark_authors, False))
        if final_bookmarks: final.insert_into_final('story_links', final_bookmarks)

    # AUTHORS
    log.info("Copying authors to final table {0}.authors, cleaning emails and removing authors with no works...".format(
        args.output_database))
    final_authors = []
    authors = final.original_table(table_names['authors'])
    for final_author in authors:
        if any(story['author_id'] == final_author['id'] or story['coauthor_id'] == final_author['id'] for story in
               final_stories) \
                or any(bookmark['author_id'] == final_author['id'] for bookmark in final_bookmarks):
            final_author['email'] = _clean_email(final_author)
            final_authors.append(final_author)
    final.insert_into_final('authors', final_authors)

    # CHAPTERS
    chapters = final.original_table(table_names['chapters'], '')
    if chapters:
        dest_chapter_table = f"{args.output_database}.{table_names['chapters']}"
        log.info("Copying chapters table {0} from source chapters table...".format(dest_chapter_table))
        sql.execute("drop table if exists {0}".format(dest_chapter_table))

        truncate_and_insert = "create table {0} (unique(id), key(story_id)) select * from {1}.{2}".format(
            dest_chapter_table,
            args.temp_db_database,
            table_names['chapters'])
        sql.execute(truncate_and_insert)

        add_auto_increment = "alter table {0} modify id int not null auto_increment".format(dest_chapter_table)
        sql.execute(add_auto_increment)
    else:
        log.info("Creating chapters table {0}.chapters from source stories table...".format(args.output_database))
        final_chapters = final.dummy_chapters(final_stories)
        final.insert_into_final('chapters', final_chapters)

if __name__ == "__main__":
    args_obj = Args()
    args = args_obj.args_for_05()
    log = args_obj.logger_with_filename()
    main(args, log)