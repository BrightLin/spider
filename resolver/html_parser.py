from bs4 import BeautifulSoup


class Parser:
    def parse(self, new_url, html_doc):
        if new_url is None or html_doc is None:
            return

        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
