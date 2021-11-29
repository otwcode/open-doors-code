import logging
import sys
import os
from colorlog import ColoredFormatter

logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.DEBUG)

def logger(filename):
  log = logging.getLogger()
  log.setLevel(logging.INFO)

  color_formatter = ColoredFormatter('%(log_color)s%(message)s%(reset)s')
  stream = logging.StreamHandler(sys.stdout)
  stream.setLevel(logging.INFO)
  stream.setFormatter(color_formatter)
  log.addHandler(stream)

  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  fh = logging.FileHandler("{0}.log".format(filename))
  fh.setFormatter(formatter)
  log.addHandler(fh)
  return log
