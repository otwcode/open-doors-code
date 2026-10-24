from bs4 import BeautifulSoup as bs


class LinkParser:
    def __init__(self, filetext):
        self.filetext = filetext

    def _is_relative(self, link):
        if link.startswith(".") or link.startswith("/"):
            return True
        elif not link.startswith("http"):
            return True
        else:
            return False

    def extract_links(self):
        soup = bs(self.filetext, "html.parser")
        links = [
            l.get("href")
            for l in soup.find_all("a", href=True)
            if not self._is_relative(l.get("href"))
        ]
        for i in soup.find_all("img"):
            if not self._is_relative(i.get("src")):
                links.append(i.get("src"))
        return links