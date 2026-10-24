import csv
import os

from shared_python.Args import Args
from shared_python.Common import print_progress, recursive_story_listdir
from shared_python.Logging import logger
from shared_python.Parsers import LinkParser
from shared_python.Requests import RequestHandler


args_obj = Args()
args = args_obj.args_for_link_check()
log = args_obj.logger_with_filename()
handler = RequestHandler()

story_files_folder = args.chapters_path
output_folder = args.output_folder
file_encoding = input(
    "Enter encoding of the story files (leave blank for utf-8):\n"
).lower()
if file_encoding == "":
    file_encoding = "utf-8"

stories = recursive_story_listdir(story_files_folder)
log.info(f"Preparing to parse through {len(stories)} stories")

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
    cur = 0
    for s in stories:
        try:
            with open(
                f"{story_files_folder}/{s}", mode="r", encoding=file_encoding
            ) as f:
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
        except UnicodeDecodeError:
            log.info(f"\nencoding error with story file {s}")
            writer.writerow(
                {
                    "story_id": s.split(".")[0],
                    "link": link,
                    "response": "read error",
                    "redirect_location": "",
                    "redirect_response": "",
                }
            )
        cur += 1
        print_progress(cur, len(stories), "stories parsed")
