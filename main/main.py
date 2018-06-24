# coding:utf-8
from downloader import html_downloader
from manager import url_manager
from outputer import data_outputer
from resolver import html_parser

url = "http://g.beva.com/kan-erge/c10266.html#1905"


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.htmlDownloader = html_downloader.Downloader()
        self.htmlParser = html_parser.Parser()
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
                new_urls, new_data = self.htmlParser.parse(new_url, html_doc)
                # 添加urls
                self.urls.add_new_urls(new_urls)
                # 添加数据
                self.outer.collect_data(new_data)

                if count == 1:
                    break

                count = count + 1
            except Exception as e:
                print("craw fail. ", e)

        # 输出数据
        self.outer.output_data()


if __name__ == "__main__":
    spider = SpiderMain()
    spider.craw(url)
