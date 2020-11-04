import scrapy
import json
import time
import os
import random

class BangumilistSpider(scrapy.Spider):
    name = "bangumilist"

    bangumilist_filename = '/home/charlie/bilibilispider/danmu/data/bangumi_all.json'

    bangumi_all_list = []

    start_urls = ['https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1']

    # def start_requests(self):
    #     first_page = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1'
    #     yield scrapy.Request(url=first_page, callback=self.parse)

    def parse(self, response):
        body = json.loads(response.body)
        one_page_list = body['data']['list']
        self.bangumi_all_list += one_page_list

        if body['data']['has_next']:
            next_page_num = int(body['data']['num']) + 1
            next_page = f'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page={next_page_num}&season_type=1&pagesize=20&type=1'
            time.sleep(0.1+0.1*random.random())
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            with open(self.bangumilist_filename, 'w') as f:
                json.dump(self.bangumi_all_list, fp = f, ensure_ascii = False, indent = 2)
            self.log(f'Saved file {self.bangumilist_filename}')