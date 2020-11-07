'''
Author : charlie
Version: 1.0

TODO:
1. supplement more sensitive words
2. add confidence estimation
3. Merge adjacent time points
4. Data noise reduction

'''

import os
import json
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from texttable import Texttable

sensitive_words = ['圣光', '圣骑', '暗牧', '马赛克', '打码', '图P', 'P图', '删', '画面裁剪', 
                '去去就来', '学成归来', '港澳', '一国两制',
                '血是绿色', '血是黑色', '血是蓝色', '血是灰色', 
                '青少年模式', '付费模式',
                '无性生殖', '无性繁殖', '有丝分裂']

insensitive_words = ['克隆', '植物', '删除', '删号', '删好友']

area_words = ['僅限']

def check(danmu):
    for aw in area_words:
        if aw in danmu['bangumi_season']:
            return False
    for iw in insensitive_words:
        if iw in danmu['text']:
            return False
    for sw in sensitive_words:
        if sw in danmu['text']:
            return True
    return False

def customed_key(x):
    EPISODE_INT = 1000000
    MAX_INT = 100000000
    try:
        bangumi_episode_num = float(x['bangumi_episode_num'])
        return bangumi_episode_num * EPISODE_INT + x['appear_timestamp']
    except:
        return MAX_INT + x['appear_timestamp']

def convert(str):
    new_string = ""
    for c in str:
        if ord(c) <= 126:
            new_string += chr(ord(c) + 65248)
        else:
            new_string += c
    return new_string

if __name__ == "__main__":
    
    print("Detecting Bilibili Malicious Cuts...")

    for sw in sensitive_words:
        print(sw)

    print("Welcome to add more sensitive words to this list...")

    bangumicomment_dirname = '/home/charlie/bilibilispider/danmu/data/comment/'
    bangumiresult_filename = '/home/charlie/bilibilispider/danmu/data/result_suspect.md'
    json_postfix = '.json'

    # results = PrettyTable()
    # results.field_names = ["Season", "Episode", "Time", "Confidence", "Danmu"]
    # results._min_width = {"Season" : 50, "Danmu" : 50}
    # results._max_width = {"Season" : 70, "Danmu" : 70}

    # results_without_text = PrettyTable()
    # results_without_text.field_names = ["Season", "Episode", "Time", "Confidence"]
    
    results = [["Season", "Episode", "Time", "Confidence", "Danmu"]]

    bangumi_seasons = os.listdir(bangumicomment_dirname)
    for bangumi_season in bangumi_seasons:
        sensitive_danmu = []

        bangumi_season_path = os.path.join(bangumicomment_dirname, bangumi_season)
        bangumi_episodes = os.listdir(bangumi_season_path)
        for bangumi_episode in bangumi_episodes:
            if json_postfix in bangumi_episode:
                bangumi_episode_path = os.path.join(bangumi_season_path, bangumi_episode)
                bangumi_episode = bangumi_episode[:-len(json_postfix)]

                with open(bangumi_episode_path, 'r') as f:
                    danmu_list = json.load(fp = f)
                for danmu in danmu_list:
                    if check(danmu):
                        sensitive_danmu.append(danmu)

        sensitive_danmu.sort(key=customed_key)
        
        last_danmu = {'bangumi_season': None, 'bangumi_episode': None, 'appear_timestamp': 0}
        
        for i in range(len(sensitive_danmu)):
            danmu = sensitive_danmu[i]
            if danmu['bangumi_season'] != last_danmu['bangumi_season'] or danmu['bangumi_episode'] != last_danmu['bangumi_episode'] or danmu['appear_timestamp'] - last_danmu['appear_timestamp'] > 120:
                results.append([danmu['bangumi_season'], danmu['bangumi_episode'], danmu['appear_time'], "TODO", danmu['text']])
                # results.add_row([danmu['bangumi_season'], danmu['bangumi_episode'], danmu['appear_time'], "TODO", danmu['text']])
            last_danmu = danmu
            
        # for danmu in sensitive_danmu:

            # danmu['bangumi_season'] = convert(danmu['bangumi_season'])
            # danmu['bangumi_episode'] = convert(danmu['bangumi_episode'])
            # danmu['appear_time'] = convert(danmu['appear_time'])
            # danmu['text'] = convert(danmu['text'])

            

    with open(bangumiresult_filename, 'w') as f:
        # print(results, file = f)
        for i in range(len(results[0])):
            f.write('| ' + str(results[0][i]) + ' ')
        f.write('|\n| :------: | - | - | - | - |\n')
        for i in range(1, len(results)):
            for j in range(len(results[i])):
                f.write('| ' + str(results[i][j]) + ' ')
            f.write('|\n')
            
            
