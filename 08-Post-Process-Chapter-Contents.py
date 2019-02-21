from post_processing.mysql_chapters import MysqlChapters
from shared_python.Args import Args

if __name__ == "__main__":
  """
  After loading the chapters into the database, export the chapters table into a SQL dump and run this script on it.
  """
  args = Args().args_for_02()
  images_file = "{0}_images.txt".format(args.archive_short_name)
  chapters = MysqlChapters(args.chapters_sql_dump)
  print chapters.check_for_broken_unicode()
  chapters.fix_unicode()
  chapters.extract_images(images_file)
