import logging
import sys

logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.DEBUG)

log = logging.getLogger()

fh = logging.FileHandler("imports.log")
log.addHandler(fh)