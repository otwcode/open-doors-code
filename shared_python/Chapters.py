import codecs
import os
import re

from pip._vendor.distlib.compat import raw_input
from pymysql import MySQLError

from shared_python import Common


# TODO this code is no longer needed for eFiction and will need to be reviewed for other archive types
class Chapters:
    def __init__(self, args, sql, log):
        self.args = args
        self.sql = sql
        self.log = log

    def _ends_with(self, filename, extensions):
        return any(filename.endswith(ext) for ext in extensions)

    def _gather_and_dedupe(self, chapters_path, extensions, has_ids=False):
        self.log.info("\nFinding chapters and identifying duplicates")
        extensions = re.split(r", ?", extensions)
        story_folder = os.walk(chapters_path)
        file_paths = {}
        duplicate_chapters = {}
        has_duplicates = False
        messages = []
        sql_messages = []
        cur = 0

        for root, _, filenames in story_folder:
            total = len(filenames)
            Common.print_progress(cur, total)

            for filename in filenames:
                if has_ids and self._ends_with(filename, extensions):
                    file_path = os.path.join(root, filename)
                    cid = os.path.splitext(filename)[0]
                    if cid not in file_paths:
                        file_paths[cid] = file_path
                    else:
                        duplicate_folder = os.path.split(os.path.split(file_path)[0])[1]
                        messages.append(
                            file_path + " is a duplicate of " + file_paths[cid]
                        )
                        sql_messages.append(f"SELECT * FROM chapters WHERE id = {cid}")
                        duplicate_chapters[cid] = [
                            {
                                "folder_name": os.path.split(
                                    os.path.split(file_paths[cid])[0]
                                )[1],
                                "filename": filename,
                                "path": file_paths[cid],
                            },
                            {
                                "folder_name": duplicate_folder,
                                "filename": filename,
                                "path": file_path,
                            },
                        ]
                        has_duplicates = True
                else:
                    file_path = os.path.join(root, filename)
                    name = os.path.splitext(filename)[0]
                    file_paths[name] = file_path

        if has_duplicates:
            self.log.warning("\n".join(messages + sql_messages))
            self.log.warning(duplicate_chapters)
            folder_name_type = raw_input(
                f"Resolving duplicates: pick the type of the folder name under {chapters_path} "
                "\n1 = author id\n2 = author name\n3 = skip duplicates check\n"
            )
            if folder_name_type == "1":
                for cid, duplicate in duplicate_chapters.items():
                    # look up the author id and add that one to the file_names list
                    sql_author_id = self.sql.execute_and_fetchall(
                        self.sql.database,
                        ("""SELECT author_id FROM chapters WHERE id = %s""", [cid]),
                    )
                    if len(sql_author_id) > 0:
                        author_id = sql_author_id[0][0]
                        file_paths[cid] = next(
                            dc["path"]
                            for dc in duplicate
                            if dc["folder_name"] == str(author_id)
                        )
            elif folder_name_type == "2":
                self.log.warning("Not implemented")

        return file_paths

    # TODO this is no longer needed to load eFiction chapters - see if it's still useful for other archive types
    def populate_chapters(self, folder=None, extensions=None):
        if folder is None:
            folder = self.args.chapters_path
        if extensions is None:
            extensions = self.args.chapters_file_extensions

        self.log.info("Processing chapters...")

        filenames_are_ids = raw_input("\nChapter file names are chapter ids? Y/N\n")
        has_ids = str.lower(filenames_are_ids) == "y"
        file_paths = self._gather_and_dedupe(folder, extensions, has_ids)

        char_encoding = raw_input(
            "\n\nImporting chapters: pick character encoding (check for curly quotes):\n"
            "1 = Windows 1252\nenter = UTF-8\n"
        )

        if char_encoding == "1":
            char_encoding = "cp1252"
        else:
            char_encoding = "utf8"

        cur = 0
        total = len(file_paths)

        if has_ids:
            for cid, chapter_path in file_paths.items():
                with codecs.open(chapter_path, "r", encoding=char_encoding) as c:
                    try:
                        cur = Common.print_progress(cur, total)
                        file_contents = c.read()
                        query = f"UPDATE {self.args.output_database}.chapters SET text=%s WHERE id=%s"
                        self.sql.execute(query, (file_contents, int(cid)))
                    except MySQLError as e:
                        self.log.error(
                            f"Error = chapter id: {cid} - chapter: {chapter_path}\n{e!s}"
                        )
                    finally:
                        pass
        else:
            for chapter_path in file_paths.values():
                path = chapter_path.replace(self.args.chapters_path, "")[1:]
                if os.sep == "\\":  # if this script is run on windows
                    path = path.replace("\\", "/")
                with codecs.open(chapter_path, "r", encoding=char_encoding) as c:
                    try:
                        cur = Common.print_progress(cur, total)
                        file_contents = c.read()
                        query = f"UPDATE {self.args.output_database}.chapters SET text=%s WHERE url=%s and text=''"
                        self.sql.execute(query, (file_contents, path))
                    except MySQLError as e:
                        self.log.error(
                            f"Error = chapter id: {path} - chapter: {chapter_path}\n{e!s}"
                        )
                    finally:
                        pass
