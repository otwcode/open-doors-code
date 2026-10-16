from colorama import Fore, Style


class Messaging:
    """
    class that handles interactivity, message colors, etc
    """

    def __init__(self, text):
        self.text = text
        self.summary_color = Fore.BLUE
        self.notes_color = Fore.MAGENTA
        self.warning_color = Fore.LIGHTBLUE_EX
        self.commercial_color = Fore.RED
        self.additional_lines_color = Fore.LIGHTBLACK_EX
        self.general = Fore.GREEN
        self.reset = Style.RESET_ALL

    def check_init_response(self, type):
        match type:
            case "summary":
                print(self.summary_color + f"{type}:\n" + self.reset + self.text)
            case "notes":
                print(self.notes_color + f"{type}:\n" + self.reset + self.text)
            case "warnings":
                print(self.warning_color + f"{type}:\n" + self.reset + self.text)
            case "commercial":
                print(self.commercial_color + f"{type}:\n" + self.reset + self.text)
        r = input(
            self.general
            + "Enter 'n' if this is not correct, otherwise press any key to continue: \n"
            + self.reset
        )
        if r.lower() == "n":
            return False
        return True

    def check_additional_lines(self, preview):
        print(f"{self.text}\n")
        print(self.additional_lines_color + preview + self.reset)
        r = input(
            (
                self.general
                + "Enter 'n' if you would like to add the next line to the string identified and removed, otherwise press any key to continue: \n"
                + self.reset
            )
        )
        if r == "n":
            return True
        return False
