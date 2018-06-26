import urllib.request as netlib

from pip._vendor import requests


class Downloader:

    def download_html(self, new_url):
        print("download html: ", new_url)
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;",
            "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

        req = session.get(new_url, headers=headers)
        return req.text

        #
        # response = netlib.urlopen(new_url)
        # data = response.read()
        #
        # return bytes.decode(data, encoding='utf-8')
