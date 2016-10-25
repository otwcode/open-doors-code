def print_progress(cur, total):
  cur += 1
  import sys
  sys.stdout.write('\r{0}/{1} stories'.format(cur, total))
  sys.stdout.flush()
  return cur
