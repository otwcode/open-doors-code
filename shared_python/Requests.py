import requests

# use log files and args


class RequestHandler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
        }
        self.redirect_codes = [301, 302, 307, 308]

    def _send_head(self, url):
        try:
            r = requests.head(url=url, headers=self.headers, timeout=10)
        except requests.exceptions.Timeout:
            r = "request timeout"
        except Exception as e:
            r = str(e)
        return r

    def status_code_handler(self, url):
        return_dict = {
            "status_code": "",
            "redirect_location": "",
            "redirect_response": "",
        }
        status = self._send_head(url)
        if isinstance(status, str):
            return_dict.update({"status_code": status})
        else:
            if status.status_code in self.redirect_codes:
                return_dict.update({"redirect_location": status.headers["location"]})
                redirect_status = self._send_head(status.headers["location"])
                if isinstance(redirect_status, str):
                    return_dict.update({"redirect_response": redirect_status})
                else:
                    return_dict.update(
                        {"redirect_response": redirect_status.status_code}
                    )
            return_dict.update({"status_code": status.status_code})
        return return_dict
