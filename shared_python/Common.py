# -- coding: utf-8 --
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def print_progress(cur, total, prog_type = "stories"):
  cur += 1
  import sys
  sys.stdout.write('\r{0}/{1} {2}'.format(cur, total, prog_type))
  sys.stdout.flush()
  return cur
