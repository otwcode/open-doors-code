import os
import shutil

from shared_python.Args import Args
from shared_python.Common import recursive_story_listdir

from story_cleanup.outputs import OutputCSV, OutputStoryFiles
from story_cleanup.parsing import Parser


# TODO: improve logging
"""
For archives where authors' notes and summaries are in the main body of text, this script scans for and removes them
note that this does /not/ load fields into the database tables, only extracts them to a CSV (and deletes if necessary)
"""

if __name__ == "__main__":
    args_obj = Args()
    args = args_obj.args_for_sn_extraction()
    stories = recursive_story_listdir(args.chapters_path)
    log = args_obj.logger_with_filename()

    options = args.scan_types
    to_remove = args.remove_option

    csv = OutputCSV(args.output_csv, options)
    j = int(
        input("the index you left off at, if you are starting from scratch enter 0\n")
    )

    if to_remove is not None and j == 0:
        shutil.copytree(args.chapters_path, args.chapters_backup_path)
        rewrite = OutputStoryFiles(args.chapters_path)

    try:
        # TODO: function that queries db for chapter and filenames
        if j == 0:
            csv.init_csv()
        for s in stories[j:]:
            log.info(f"story: {s}")
            fname = os.path.join(args.chapters_path, s)
            with open(fname, "r") as f:
                text = f.readlines()
            parser = Parser(text, options)
            hits = parser.parse_lines()

            if to_remove is not None:
                new_text = rewrite.strip_and_rewrite(text, hits)
                rewrite.out_to_file(s, new_text)

            hits.update({"story_identifier": s})
            csv.write_data(hits)
            j += 1

    except KeyboardInterrupt:
        print(f"progress at restart: {j}")
    except Exception as e:
        print(f"there's been an error: {e}\n")
        print(f"progress at restart: {j}")
