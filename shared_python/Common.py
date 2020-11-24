# -- coding: utf-8 --
import sys
from importlib import reload

reload(sys)
#sys.setdefaultencoding('utf8') #setdefaultencoding is disabled in Python 3. UTF-8 is also default coding.

def print_progress(cur, total, prog_type = "stories"):
  cur += 1
  import sys
  sys.stdout.write('\r{0}/{1} {2}'.format(cur, total, prog_type))
  sys.stdout.flush()
  return cur
