import http.cookiejar
import json
import re
import urllib.parse
import urllib.request
import urllib.request as netlib

from bs4 import BeautifulSoup

from resolver.html_parser import Parser

item_info_url = "http://g.beva.com/kan-erge/data-itemInfo-i#ID#.html"
item_video = "http://g.beva.com/kan/data/itemVideo?code="


class Mp4Parser(Parser):

    def parse(self, new_url, html_doc):
        if new_url is None or html_doc is None:
            return

        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(new_url, soup)
        id = self._get_mp4_id(soup)
        return new_urls, id

    def _get_mp4_id(self, soup):
        scripts = soup.findAll('script')
        for script in scripts:
            text = script.get_text()
            if text.find('window.location.search') >= 0:
                all_ids = re.findall(r'h\s*=\s*\d*', text)
                if not all_ids is None and len(all_ids) > 0:
                    for all_id in all_ids:
                        ids = re.findall(r'\d+', all_id)
                        if not ids is None and len(ids) > 0:
                            for id in ids:
                                if not id is None and id.isdigit():
                                    return id

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
            # print("get name: ", mp4_name)

        # print(soup)
        mp4_datas = set()
        vcp_player = soup.findAll('div', class_='vcp-player')
        # print("get Mp4 url: ", vcp_player)
        for res in vcp_player:
            mp4_datas.add({'url': res.video['src'], 'name': mp4_name})

        return mp4_datas

    def get_item_info_url(self, id):
        return item_info_url.replace('#ID#', id)

    def get_video_url(self, base_url, content):
        try:
            if not content is None and len(content) > 0:
                data = json.loads(content)
                item_name = data['data']['itemName']
                auth_codes = re.findall(r'\"authcode\"\s*:\s*\"[0-9a-zA-Z]*\"', content)
                if len(auth_codes) == 1:
                    auth_code = auth_codes[0].replace('"', '').split(':')[1]
                    result = self.download_video_html(item_video + auth_code, base_url)
                    mp4_url = re.findall(r'\"url\":\".*.mp4\"', result)[0]
                    mp4_url = mp4_url.replace('"', '')
                    return item_name, mp4_url[4:].replace('\\', '')
        except Exception as e:
            print(e)
            return None

    def download_video_html(self, new_url, base_url):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('Referer', base_url),
            ('Accept', 'application/json, text/javascript, */*; q=0.01'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36')]
        urllib.request.install_opener(opener)

        response = netlib.urlopen(new_url)
        data = response.read()

        return data.decode(encoding='utf-8')
