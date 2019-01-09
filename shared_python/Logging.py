import logging
import sys

logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.DEBUG)

def logger(filename):
  log = logging.getLogger()

  fh = logging.FileHandler("{0}.log".format(filename))
  log.addHandler(fh)
  return log