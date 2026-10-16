class Keywords:
    def __init__(self):
        self.notes = [
            "note",
            "a/n",
            "disclaimer",
            "tumblr",
            "author"
        ]
        self.warnings = [
            "warning",
            "cw",
            "content warning",
            "trigger warning",
            "tw",
        ]
        self.summary = [
            "summary",
            "summaries",
            "prompt",
            "synopsis"
        ]
        self.commercial = [
            "patreon",
            "ko-fi",
            "kofundme",
        ]
        # self.ratings
        # self.wordcount
        # self.pairings
        # self.characters
        # others defined

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
            case _:
                raise NameError(
                    "unsupported type: must be 'notes', 'warnings', 'summary', or 'commercial'; check config file"
                )
        for k in keywords:
        # eventually, a regex would be more efficient here, but with the line-by-line parsing built in this works for now
            if k in text.lower():
                return True
        return False
