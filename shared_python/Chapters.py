# -- coding: utf-8 --

#import codecs
import os
import re
import chardet

from pip._vendor.distlib.compat import raw_input

from shared_python import Common

# Disable useless logs from chardet
import logging
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

# TODO this code is no longer needed for eFiction and will need to be reviewed for other archive types
class Chapters(object):

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
          if cid not in file_paths.keys():
            file_paths[cid] = file_path
          else:
            duplicate_folder = os.path.split(os.path.split(file_path)[0])[1]
            messages.append(file_path + " is a duplicate of " + file_paths[cid])
            sql_messages.append("SELECT * FROM chapters WHERE id = {0}".format(cid))
            duplicate_chapters[cid] = [
              {'folder_name': os.path.split(os.path.split(file_paths[cid])[0])[1], 'filename': filename,
               'path': file_paths[cid]},
              {'folder_name': duplicate_folder, 'filename': filename, 'path': file_path}
            ]
            has_duplicates = True
        else:
          file_path = os.path.join(root, filename)
          name = os.path.splitext(filename)[0]
          file_paths[name] = file_path

    if has_duplicates:
      self.log.warn('\n'.join(messages + sql_messages))
      self.log.warn(duplicate_chapters)
      folder_name_type = raw_input("Resolving duplicates: pick the type of the folder name under {0} "
                                   "\n1 = author id\n2 = author name\n3 = skip duplicates check\n"
                                   .format(chapters_path))
      if folder_name_type == '1':
        for cid, duplicate in duplicate_chapters.items():
          # look up the author id and add that one to the file_names list
          # TODO fix this, it is missing the database 
          sql_author_id = self.sql.execute_and_fetchall("SELECT author_id FROM chapters WHERE id = {0}".format(cid))
          if len(sql_author_id) > 0:
            author_id = sql_author_id[0][0]
            file_paths[cid] = [dc['path'] for dc in duplicate_chapters[cid] if dc['folder_name'] == str(author_id)][0]
      elif folder_name_type == '2':
        self.log.warn("Not implemented")

    return file_paths

  # TODO this is no longer needed to load eFiction chapters - see if it's still useful for other archive types
  def populate_chapters(self, folder = None, extensions = None):
    if folder is None:
      folder = self.args.chapters_path
    if extensions is None:
      extensions = self.args.chapters_file_extensions

    self.log.info("Processing chapters...")

    filenames_are_ids = raw_input("\nChapter file names are chapter ids? Y/N\n")
    has_ids = True if str.lower(filenames_are_ids) == 'y' else False
    file_paths = self._gather_and_dedupe(folder, extensions, has_ids)


    cur = 0
    total = len(file_paths)

    for cid, chapter_path in file_paths.items():
      if has_ids:
        cid = int(cid)
      else:
        cid = chapter_path.replace(self.args.chapters_path, '')[1:]
      with open(chapter_path, 'rb') as raw_chapter:
        try:
          cur = Common.print_progress(cur, total)
          file_contents = raw_chapter.read()
          encoding = chardet.detect(file_contents)
          if encoding['confidence'] < 0.7:
            self.log.warn(f" Low confidence in {encoding['encoding']} in file {chapter_path}: {round(encoding['confidence'] * 100)}%")
          # Try decoding `file_contents` until it actually becomes `str`
          while isinstance(file_contents, bytes):
            try:
              file_contents = file_contents.decode(encoding=encoding['encoding'])
            except UnicodeDecodeError as e:
              self.log.warn(f"\nFailed to decode {chapter_path}")
              line_num = file_contents[:e.start].decode(encoding['encoding']).count("\n")
              print(f"At line {line_num}:\t{str(e)}")
              print("--\t", file_contents[max(e.start - 40, 0):e.end + 30])
              # print `^` under the offending byte
              print(
                      "\t",
                      " " * (len(str(file_contents[max(e.start - 40, 0):e.start])) - 1) +
                      "^" * (len(str(file_contents[e.start:e.end])) - 3)
              )
              print("Will be converted to:")
              # remove the offending bytes (usually one)
              file_contents = file_contents[:e.start] + file_contents[e.end:]
              print(
                "++\t  ",
                file_contents[
                  max(e.start - 40, 0):
                  e.end + 30
                ].decode(encoding['encoding'])
                  .replace("\n", "\\n") # escape line endings so it looks nicer
                  .replace("\r", "\\r")
                )
          query = "UPDATE {0}.chapters SET text=%s WHERE id=%s".format(self.args.output_database)
          self.sql.execute(query, (file_contents, cid))
        except Exception as e:
          self.log.error("Error = chapter id: {0} - chapter: {1}\n{2}".format(str(cid), chapter_path, str(e)))

