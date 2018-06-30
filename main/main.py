# coding:utf-8
from downloader import html_downloader
from manager import url_manager
from outputer import data_outputer
from resolver import mp4_parser

start_url = "http://g.beva.com/kan-erge/c10266.html"

MAX_count = 10


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.htmlDownloader = html_downloader.Downloader()
        self.htmlParser = mp4_parser.Mp4Parser()
        self.outer = data_outputer.Outputer()

    def craw(self, root_url):
        # 添加一个url
        self.urls.add_new_url(root_url)
        count = 1
        # 如果url管理器中有url开始循环
        while self.urls.has_new_url():
            try:
                # 获取一个新url
                new_url = self.urls.get_new_url()

                # 下载html
                html_doc = self.htmlDownloader.download_html(new_url)

                # 解析html，获取新url，和数据
                new_urls, id = self.htmlParser.parse(new_url, html_doc)
                if id == '0':
                    continue

                # 添加urls
                self.urls.add_new_urls(new_urls)

                # 获取item信息
                info_url = self.htmlParser.get_item_info_url(id)
                info_data = self.htmlDownloader.download_html(info_url)
                video_url = self.htmlParser.get_video_url(new_url, info_data)
                print('video%s: %s' % (count, video_url))

                # 添加数据
                # self.outer.collect_data(new_data)
                if count >= MAX_count:
                    break

                count = count + 1
            except Exception as e:
                print("craw fail. ", e)

        # 输出数据
        self.outer.output_data()


if __name__ == "__main__":
    spider = SpiderMain()
    spider.craw(start_url)
