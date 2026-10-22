import csv
import os

from shared_python.Args import Args
from shared_python.Common import recursive_story_listdir
from shared_python.Logging import logger
from shared_python.Parsers import LinkParser
from shared_python.Requests import RequestHandler


args_obj = Args()
args = args_obj.args_for_link_check()
log = args_obj.logger_with_filename()
handler = RequestHandler()

story_files_folder = args.chapters_path
output_folder = args.output_folder

stories = recursive_story_listdir(story_files_folder)
with open(f"{output_folder}/story_file_links.csv", "a") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "story_id",
            "link",
            "response",
            "redirect_location",
            "redirect_response",
        ],
    )
    for s in stories:
        with open(f"{story_files_folder}/{s}", "r") as f:
            story_text = f.read()
        parser = LinkParser(story_text)
        links = parser.extract_links()
        for link in links:
            response_meta = handler.status_code_handler(link)
            writer.writerow(
                {
                    "story_id": s.split(".")[0],
                    "link": link,
                    "response": response_meta["status_code"],
                    "redirect_location": response_meta["redirect_location"],
                    "redirect_response": response_meta["redirect_response"],
                }
            )
