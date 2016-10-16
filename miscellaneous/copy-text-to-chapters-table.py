# -- coding: utf-8 --

import codecs
import os
import MySQLdb

db = MySQLdb.connect("localhost","root","","$DATABASE$")
cursor = db.cursor()


thing = [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.txt')] for i in os.walk('./stories')] for val in sublist]
for chapter_path in thing:
  path_elements = chapter_path.split('/')
  stories = path_elements[1]
  author_name = path_elements[2]
  chapter_id = path_elements[-1].split('.txt')[0]

  with codecs.open(chapter_path, 'r', encoding='cp1252') as c:
    try:
      file_contents = c.read()
      query = "UPDATE $DATABASE$.$PREFIX$_chapters SET text=%s WHERE id=%s"
      cursor.execute(query, (file_contents, int(chapter_id)))
      db.commit()
    except Exception as e:
      print("Error = author: {0} - chapter: {1}\n{2}".format(author_name, chapter_id, str(e)))
    finally:
      pass

db.close()
