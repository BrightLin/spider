import os
import time

from pip._vendor import requests


class Outputer:
    def __init__(self):
        self.mp4_urls = {}
        self.data_path = 'out'

    def collect_data(self, item_name, item_url):
        if not item_name is None and len(item_name) > 0:
            # print('Add: %s, %s'%(item_name, item_url))
            self.mp4_urls[item_name] = item_url

    def output_data(self):
        try:
            for mp4_name in self.mp4_urls:
                self.download_data(mp4_name, self.mp4_urls[mp4_name])
                time.sleep(3)
        except:
            print("output_data error...")

    def download_data(self, name, url):
        print('Start download %s' % name)
        out_dir = os.path.join(os.getcwd(), '..', self.data_path)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        request = requests.get(url)
        file_path = os.path.join(out_dir, name + '.mp4')
        if not os.path.exists(file_path):
            data_out = open(file_path, 'wb')
            data_out.write(request.content)
            data_out.close()
            print('Download success: %s' % name)
        else:
            print('%s exists.' % name)
