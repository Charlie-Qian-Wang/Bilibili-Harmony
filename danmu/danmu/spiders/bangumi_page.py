import scrapy
import json
import time
import os
import random
from bs4 import BeautifulSoup

class BangumiPageSpider(scrapy.Spider):
    name = "bangumipage"

    bangumipage_dirname = '/home/charlie/bilibilispider/danmu/data/page/'
    bangumilist_filename = '/home/charlie/bilibilispider/danmu/data/bangumi_all.json'
    html_postfix = '.html'
    json_postfix = '.json'
    keystring = 'window.__INITIAL_STATE__='
    keyendl = ';'

    def start_requests(self):

        with open(self.bangumilist_filename, 'r') as f:
            bangumi_all_list = json.load(fp = f)

        for bangumi in bangumi_all_list:
            time.sleep(0.1+0.1*random.random())
            yield scrapy.Request(url = bangumi['link'], meta = bangumi, callback = self.parse)

    def parse(self, response):

        filename = os.path.join(self.bangumipage_dirname, str(response.meta['season_id']) + self.html_postfix)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_string = soup.prettify()
        with open(filename, 'w') as f:
            f.write(soup.prettify())
            self.log(f'Saved file {filename}')

        if response.status != 200:
            return

        content_list = response.css('script::text').getall()
        content_list = [s[len(self.keystring):s.find(self.keyendl)] for s in content_list if self.keystring in s]
        content = json.loads(content_list[0])

        filename = os.path.join(self.bangumipage_dirname, str(response.meta['season_id']) + self.json_postfix)
        with open(filename, 'w') as f:
            json.dump(content, fp = f, ensure_ascii = False, indent = 2)
            self.log(f'Saved file {filename}')
        