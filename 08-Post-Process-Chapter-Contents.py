from post_processing.mysql_chapters import MysqlChapters
from shared_python.Args import Args
from shared_python.Sql import Sql

if __name__ == "__main__":
  """
  After loading the chapters into the database, export the chapters table into a SQL dump and run this script on it.
  """
  argsClass = Args()
  args = argsClass.args_for_02()
  log = argsClass.logger_with_filename()
  sql = Sql(args, log)

  images_file = "{0}_images.txt".format(args.archive_short_name)
  links_file = "{0}_links.txt".format(args.archive_short_name)
  chapters = MysqlChapters(args.chapters_sql_dump)
  if chapters.check_for_broken_unicode():
    chapters.fix_unicode()
  chapters.extract_images(images_file)
  chapters.extract_links(links_file)
  chapters.html_report(links_file)