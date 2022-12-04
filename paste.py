import requests
import urllib.parse


class KlgrthPaste:
    def __init__(self):
        pass

    def paste(self, text):
        r = requests.post(
            "https://www.klgrth.io/paste/new",
            data={
                "text": text,
                "lang": "text",
                "expire": -1,
                "password": "",
                "title": "",
            },
            allow_redirects=False,
        )
        return self.__raw_url(r.headers["Location"])

    def __raw_url(self, url):
        url = urllib.parse.urljoin("https://www.klgrth.io/", url)
        return url + "/raw"


# if __name__ == "__main__":
#     klgrth = KlgrthPaste()
#     print(klgrth.paste("hello world 123"))
