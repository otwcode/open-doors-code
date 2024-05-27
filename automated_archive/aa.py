# -- coding: utf-8 --

import datetime
import codecs
import re
from pathlib import Path
from html.parser import HTMLParser

from pymysql import connect

from shared_python import Args, Common
from shared_python.Sql import Sql


def _escape_quote(text):
    return text.replace("(?<!\\)'", "\\'")


def _clean_file(filepath, log):
    """
    Convert the Perl hash into a Python dictionary
    :param filepath: Path to ARCHIVE_DB.pl
    :return: Python dictionary keyed by original story id
    """
    h = HTMLParser()
    archive_db = codecs.open(filepath, "r", encoding="utf-8").read()

    # Manually escape single quote entity and reformat file as a Python dictionary
    step1 = h.unescape(archive_db.replace("&#39;", "\\&#39;"))

    # Indent the file with a single tab instead of whatever is currently used
    step15 = re.sub(r"^\s+", "\t", step1)

    step2 = (
        step15.replace("%FILES = (\n\n", '{\n"')
        .replace("\n)", "\n}")
        .replace("},\n", '},\n"')
        .replace("\t\n", "")
        .replace("\t", '\t"')
        .replace(" =>", '":')
        .replace(";\n", ",\n")
        .replace(',\n"\n},\n1,', "}")
    )
    # Replace line breaks within fields (followed by a character that isn't a space, tab, digit, } or ")
    step3 = re.sub(r"\n(?=[^ \t\d\}\"])", " ", step2)

    # Edit these to fix dodgy data specific to this archive
    final_replace = step3.replace("0,/2,/25", "01/30/00").replace(
        "\t\"PrintTime\": 'P',\n", ""
    )
    final_regex = re.sub(r"00,02,\d(.*?)',", "02/26/00',", final_replace)

    archive_db_python = eval(final_regex)

    # List fields in AA db file
    keys = [dict.keys() for dict in archive_db_python.values()]
    unique_keys = set([val for sublist in keys for val in sublist])
    log.info(
        "Fields in ARCHIVE_DB.pl: {0}".format(", ".join(str(e) for e in unique_keys))
    )

    return archive_db_python


def _is_external(record):
    """
    AA is pretty flexible - define the bookmark criteria here, whatever it is
    :param record:
    :return: whether this record is an external link
    """
    # Spooky 2003
    # return record.get('Offsite', 'none') != 'none'
    # or record.get('FileType', 'none') == 'none' \
    # Spooky 2004
    # return record.get('Offsite', 'none') == 'offsite'
    # Spooky 2005
    return record.get("LocationURL", "").startswith("http")


def _extract_tags(args, record):
    tags = ""
    if args.tag_fields is not None:
        for tag_field in args.tag_fields.split(", "):
            tags += (
                record.get(tag_field, "").replace("'", "\\'").replace('"', '\\"') + ", "
            )
    return tags.strip(", ")


def _extract_characters(args, record):
    tags = ""
    if args.character_fields is not None:
        for character_field in args.character_fields.split(", "):
            tags += (
                record.get(character_field, "").replace("'", "\\'").replace('"', '\\"')
                + ", "
            )
    return tags.strip(", ")


def _extract_relationships(args, record):
    tags = ""
    if args.relationship_fields is not None:
        for relationship_field in args.relationship_fields.split(", "):
            tags += (
                record.get(relationship_field, "")
                .replace("'", "\\'")
                .replace('"', '\\"')
                + ", "
            )
    return tags.strip(", ")


def _extract_fandoms(args, record):
    tags = ""
    if args.fandom_fields is not None:
        for fandom_field in args.fandom_fields.split(", "):
            tags += (
                record.get(fandom_field, "").replace("'", "\\'").replace('"', '\\"')
                + ", "
            )
    return tags.strip(", ")


def _create_mysql(args, FILES, log):
    db = connect(host=args.db_host, user=args.db_user, password=args.db_password, db="")
    cursor = db.cursor()
    DATABASE_NAME = args.temp_db_database

    # Use the database and empty all the tables
    cursor.execute("drop database if exists {0};".format(DATABASE_NAME))
    cursor.execute("create database {0};".format(DATABASE_NAME))
    cursor.execute("use {0}".format(DATABASE_NAME))

    sql = Sql(args, log)
    script_path = (
        Path(__file__).parent.parent / "shared_python" / "create-open-doors-tables.sql"
    )

    sql.run_script_from_file(script_path, database=DATABASE_NAME)
    db.commit()

    authors = [
        (
            FILES[i].get("Author", "").strip(),
            FILES[i].get("Email", FILES[i].get("EmailAuthor", "")).lower().strip(),
        )
        for i in FILES
    ]
    auth = "INSERT INTO authors (name, email) VALUES(%s, %s);"
    cursor.executemany(auth, set(authors))
    db.commit()

    # Authors
    auth = "SELECT * FROM authors;"
    cursor.execute(auth)
    db_authors = cursor.fetchall()

    # Stories and bookmarks
    stories = [
        (
            i,
            FILES[i].get("Title", "").replace("'", "\\'"),
            FILES[i].get("Summary", "").replace("'", "\\'"),
            _extract_tags(args, FILES[i]),
            _extract_characters(args, FILES[i]),
            datetime.datetime.strptime(
                FILES[i].get(
                    "PrintTime",
                    FILES[i].get(
                        "DatePrint",
                        FILES[i].get(
                            "Date", str(datetime.datetime.now().strftime("%m/%d/%y"))
                        ),
                    ),
                ),
                "%m/%d/%y",
            ).strftime("%Y-%m-%d"),
            FILES[i].get("Location", "").replace("'", "\\'"),
            FILES[i]
            .get("LocationURL", FILES[i].get("StoryURL", ""))
            .replace("'", "\\'"),
            FILES[i].get("Notes", "").replace("'", "\\'"),
            _extract_relationships(args, FILES[i]),
            FILES[i].get("Rating", ""),
            FILES[i].get("Warnings", "").replace("'", "\\'"),
            FILES[i].get("Author", "").strip(),
            FILES[i].get("Email", FILES[i].get("EmailAuthor", "")).lower().strip(),
            FILES[i].get("FileType", args.chapters_file_extensions)
            if not _is_external(FILES[i])
            else "bookmark",
            _extract_fandoms(args, FILES[i]),
        )
        for i in FILES
    ]

    cur = 0
    total = len(FILES)
    for (
        original_id,
        title,
        summary,
        tags,
        characters,
        date,
        location,
        url,
        notes,
        pairings,
        rating,
        warnings,
        author,
        email,
        filetype,
        fandoms,
    ) in set(stories):
        cur = Common.print_progress(cur, total)
        try:
            # For AA archives with external links:
            if filetype != "bookmark":
                if location == "":
                    filename = url
                else:
                    filename = location + "." + filetype
                table_name = "stories"
            else:
                filename = url
                table_name = "bookmarks"

            # Clean up fandoms and add default fandom if it exists
            final_fandoms = fandoms.replace("'", r"\'")
            if args.default_fandom is not None:
                if final_fandoms == "" or final_fandoms == args.default_fandom:
                    final_fandoms = args.default_fandom
                else:
                    final_fandoms = args.default_fandom + ", " + final_fandoms

            result = [
                element
                for element in db_authors
                if element[1] == author and element[2] == email
            ]
            authorid = result[0][0]

            stor = """
        INSERT INTO {0} (id, fandoms, title, summary, tags, characters, date, url, notes, relationships, rating, warnings, author_id)
        VALUES({1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}');\n""".format(
                table_name,
                original_id,
                final_fandoms.replace(r"\\", "\\"),
                title.replace(r"\\", "\\"),
                summary,
                tags,
                characters,
                date,
                filename,
                notes,
                pairings,
                rating,
                warnings,
                authorid,
            )
            cursor.execute(stor)
        except:
            log.error(
                "table name: {0}\noriginal id: {1}\nfinal fandoms: '{2}'\ntitle: '{3}'\nsummary: '{4}'\ntags: '{5}'"
                "\ncharacters: '{6}'\ndate: '{7}'\nfilename: '{8}'\nnotes: '{9}'\npairings: '{10}'\nrating: '{11}'"
                "\nwarnings: '{12}'\nauthor id: '{13}'".format(
                    table_name,
                    original_id,
                    final_fandoms,
                    title,
                    summary,
                    tags,
                    characters,
                    date,
                    filename,
                    notes,
                    pairings,
                    rating,
                    warnings,
                    authorid,
                )
            )
            raise
    db.commit()


def clean_and_load_data(args, log):
    data = _clean_file(args.db_input_file, log)
    _create_mysql(args, data, log)


if __name__ == "__main__":
    args = Args().process_args()
    data = _clean_file(args.filepath)
