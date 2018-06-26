from bs4 import BeautifulSoup

from resolver.html_parser import Parser


class Mp4Parser(Parser):

    def parse(self, new_url, html_doc):
        if new_url is None or html_doc is None:
            return

        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(new_url, soup)
        new_datas = self._get_new_data(new_url, soup)
        return new_urls, new_datas

    def _get_new_urls(self, new_url, soup):
        new_urls = set()
        pic_item = soup.findAll('div', class_='pic-item')
        for res in pic_item:
            href = res.div.a['href']
            if href.find('kan-erge') >= 0:
                new_urls.add(res.div.a['href'])

        return new_urls

    def _get_new_data(self, new_url, soup):
        mp4_name = ''
        nav_center = soup.findAll('nav', class_='center')
        for res in nav_center:
            mp4_name = res.b.get_text()
            print("get name: ", mp4_name)

        print(soup)
        mp4_datas = set()
        vcp_player = soup.findAll('div', class_='vcp-player')
        print("get Mp4 url: ", vcp_player)
        for res in vcp_player:
            mp4_datas.add({'url': res.video['src'], 'name': mp4_name})

        return mp4_datas
