import urllib.request as netlib


class Downloader:

    def download_html(self, new_url):
        response = netlib.urlopen(new_url)
        data = response.read()
        return bytes.decode(data, encoding='utf-8')
