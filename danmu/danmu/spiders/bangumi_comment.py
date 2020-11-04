import scrapy
import json
import time
import os
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class BangumiCommentSpider(scrapy.Spider):
    name = "bangumicomment"

    bangumipage_dirname = '/home/charlie/bilibilispider/danmu/data/page/'
    bangumicomment_dirname = '/home/charlie/bilibilispider/danmu/data/comment/'
    bangumilist_filename = '/home/charlie/bilibilispider/danmu/data/bangumi_all.json'
    html_postfix = '.html'
    json_postfix = '.json'
    xml_postfix = '.xml'
    keystring = 'window.__INITIAL_STATE__='
    keyendl = ';'
    comment_api = 'https://comment.bilibili.com/'
    header = {}
    
    ua = UserAgent()

    def start_requests(self):

        with open('/home/charlie/bilibilispider/verified_1.txt', 'r') as f:
            PROXIES = f.readlines()

        files = os.listdir(self.bangumipage_dirname)
        for file in files:
            if self.json_postfix in file:
                with open(os.path.join(self.bangumipage_dirname, file), 'r') as f:
                    bangumi = json.load(fp = f)
                    ep_list = bangumi['epList']
                    del bangumi['epList']

                    for ep in ep_list:
                        
                        bangumi_danmu_path = os.path.join(self.bangumicomment_dirname, str(bangumi['mediaInfo']['ssId']), str(ep['title']) + self.json_postfix)
                        if os.path.exists(bangumi_danmu_path):
                            self.log(f"Existing Path: {bangumi_danmu_path}")
                            continue
                        
                        url = self.comment_api + str(ep['cid']) + '.xml'
                        # proxy = 'http://' + random.choice(PROXIES).strip()
                        useragent = self.ua.random
                        # self.log(f"Proxy: {proxy} User-Agent: {useragent}")
                        time.sleep(5 + 1*random.random())
                        
                        yield scrapy.Request(url = url, meta = {'bangumi':bangumi, 'ep': ep}, headers = {'User-Agent': useragent}, callback = self.parse)

    def parse(self, response):

        bangumi_season = response.meta['bangumi']['h1Title']
        bangumi_season_id = response.meta['bangumi']['mediaInfo']['ssId']
        bangumi_season_path = os.path.join(self.bangumicomment_dirname, str(bangumi_season_id))

        if not os.path.exists(bangumi_season_path):
            os.makedirs(bangumi_season_path)

        bangumi_episode = response.meta['ep']['titleFormat']
        bangumi_episode_num = response.meta['ep']['title']
        bangumi_episode_path = os.path.join(bangumi_season_path, str(bangumi_episode_num) + self.xml_postfix)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_string = soup.prettify()
        with open(bangumi_episode_path, 'w') as f:
            f.write(soup.prettify())
            self.log(f'Saved file {bangumi_episode_path}')

        item_list = soup.find_all('d')
        danmu_list = []
        for item in item_list:
            danmu = {}
            attributes = item['p'].split(',')

            danmu['bangumi_season'] = bangumi_season
            danmu['bangumi_episode'] = bangumi_episode
            danmu['bangumi_episode_num'] = bangumi_episode_num
            danmu['appear_timestamp'] = float(attributes[0])
            danmu['mode'] = int(attributes[1])
            danmu['size'] = int(attributes[2])
            danmu['color'] = int(attributes[3])
            danmu['send_timestamp'] = int(attributes[4])
            danmu['danmu_pool'] = int(attributes[5])
            danmu['user_hash'] = str(attributes[6])
            danmu['global_id'] = int(attributes[7])
            danmu['text'] = item.text

            danmu['second'] = int(danmu['appear_timestamp'])
            danmu['minute'] = danmu['second'] // 60
            danmu['second'] = danmu['second'] % 60
            danmu['hour'] = danmu['minute'] // 60
            danmu['minute'] = danmu['minute'] % 60
            temp_time = str(danmu['second']) + "秒"
            if danmu['minute'] > 0:
                temp_time = str(danmu['minute']) + "分" + temp_time
            if danmu['hour'] > 0:
                temp_time = str(danmu['hour']) + "时" + temp_time
            danmu['appear_time'] = temp_time

            danmu_list.append(danmu)
        
        bangumi_danmu_path = os.path.join(bangumi_season_path, str(bangumi_episode_num) + self.json_postfix)
        with open(bangumi_danmu_path, 'w') as f:
            json.dump(danmu_list, fp = f, ensure_ascii = False, indent = 2)
            self.log(f'Saved file {bangumi_danmu_path}')