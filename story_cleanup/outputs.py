import csv
import os


class OutputCSV:
    def __init__(self, filename: str, columns: list):
        self.filename = filename
        self.columns = columns + ["story_identifier"]

    def init_csv(self):
        with open(self.filename, "w", encoding="utf_8_sig", newline="") as fp:
            csvf = csv.DictWriter(fp, fieldnames=self.columns)
            csvf.writeheader()

    def write_data(self, data: dict):
        with open(self.filename, "a", encoding="utf_8_sig", newline="") as f:
            csvf = csv.DictWriter(f, fieldnames=self.columns)
            csvf.writerow(data)


class OutputStoryFiles:
    def __init__(self, output_path):
        self.output_path = output_path

    def strip_and_rewrite(self, text, options: dict):
        text = "".join(text)
        for o in options.keys():
            hit_lines = options[o].split("\n")
            for h in hit_lines:
                text = text.replace(h, "")
        return text

    def out_to_file(self, filename, strippedtext):
        with open(os.path.join(self.output_path, filename), "w") as f:
            f.write(strippedtext)
