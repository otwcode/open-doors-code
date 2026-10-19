class Keywords:
    def __init__(self, additional_keywords={}):
        self.notes = ["note", "a/n", "disclaimer", "tumblr", "author"]
        self.warnings = [
            "warning",
            "cw",
            "content warning",
            "trigger warning",
            "tw",
        ]
        self.summary = ["summary", "summaries", "prompt", "synopsis"]
        self.commercial = [
            "patreon",
            "ko-fi",
            "kofundme",
        ]
        self.rating = ["rating", "rated"]
        self.wordcount = [
            "words",
            "words",
            "wordcount",
            "word count",
        ]
        self.pairings = ["pairing", "relationship"]

        self.additional_keywords = additional_keywords

    def _open_file_and_read(self, keywordfile):
        with open(keywordfile, "r") as f:
            words = f.readlines()
        return words

    def append_additional_keywords(self):
        for t in self.additional_keywords.keys():
            words = self._open_file_and_read(self.additional_keywords[t])
            match t:
                case "notes":
                    self.notes.append(words)
                case "warnings":
                    self.warnings.append(words)
                case "summary":
                    self.summary.append(words)
                case "rating":
                    self.ratings.append(words)
                case "wordcount":
                    self.wordcount.append(words)
                case "pairings":
                    self.pairings.append(words)

    def detect(self, type, text):
        match type:
            case "notes":
                keywords = self.notes
            case "warnings":
                keywords = self.warnings
            case "summary":
                keywords = self.summary
            case "commercial":
                keywords = self.commercial
            case "rating":
                keywords = self.ratings
            case "wordcount":
                keywords = self.wordcount
            case "pairings":
                keywords = self.pairings
            case _:
                raise NameError(
                    "unsupported type: must be 'notes', 'warnings', 'summary', 'rating', 'pairings', 'wordcount', or 'commercial'; check config file"
                )
        for k in keywords:
            if k in text.lower():
                return True
        return False
