from .keywords import Keywords
from .messages import Messaging


class Parser:
    def __init__(self, textlines: list, options: list):
        self.textlines = textlines
        self.max = len(self.textlines)
        self.options_dict = {}
        for opt in options:
            self.options_dict.update({opt: ""})
        self.end_message = "***no more lines to preview, press enter to continue***"
        self.kwords = Keywords()

    def detection_loop(self, type: str, i: int):
        m = Messaging(self.textlines[i])
        if m.check_init_response(type):
            local_count = i + 1
            txt = self.textlines[i]
            try:
                a = m.check_additional_lines(self.textlines[local_count])
            except IndexError:
                input(self.end_message)
                return txt
            while a and local_count < self.max:
                preview = self.textlines[local_count + 1]
                txt = txt + self.textlines[local_count]
                a = m.check_additional_lines(preview)
                local_count += 1
            return txt
        return ""

    def parse_lines(self):
        # this is per story file
        for i in range(0, int(self.max)):
            for o in self.options_dict.keys():
                if self.kwords.detect(o, self.textlines[i]):
                    self.options_dict[o] = (
                        self.options_dict[o] + "\n" + self.detection_loop(o, i)
                    )
        return self.options_dict
