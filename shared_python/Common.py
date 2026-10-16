# -- coding: utf-8 --
from importlib import reload
import os
import sys

reload(sys)
# sys.setdefaultencoding('utf8') #setdefaultencoding is disabled in Python 3. UTF-8 is also default coding.


def print_progress(cur, total, prog_type="stories"):
    cur += 1
    import sys

    sys.stdout.write("\r{0}/{1} {2}".format(cur, total, prog_type))
    sys.stdout.flush()
    return cur


def recursive_story_listdir(main_path):
    storyfiles = [
        x.name for x in os.scandir(main_path) if "html" in x.name or "txt" in x.name
    ]
    subdirs = [x.name for x in os.scandir(main_path) if x.is_dir()]
    for dir in subdirs:
        stories = [
            x
            for x in os.listdir(os.path.join(main_path, dir))
            if "html" in x or "txt" in x
        ]
        for s in stories:
            storyfiles.append(os.path.join(dir, s))
    return storyfiles
