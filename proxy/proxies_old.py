# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests


class Proxies(object):

    """docstring for Proxies"""

    def __init__(self, page=32):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()

    def get_proxies(self):
        page = random.randint(1, 32)
        page_stop = page + self.page
        test_url = 'https://202020.ip138.com'
        while page < page_stop:
            print("Page %d" % page)
            url = 'http://www.66ip.cn/%d.html' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'html.parser')
            ip_list = soup.find_all("table")
            if len(ip_list) < 1:
                continue
            # print(ip_list[-1])
            for odd in ip_list[-1].find_all("tr"):
                tds = odd.find_all('td')
                if len(tds) < 1:
                    continue
                if tds[0].get_text() == 'ip':
                    continue
                ip = tds[0].get_text() + ':' + tds[1].get_text()
                protocol = 'https'
                try:
                    proxy_host = protocol + '://' + ip
                    # print(proxy_host)
                    html = requests.get(test_url, proxies={protocol: proxy_host}, timeout=3)
                    if html.status_code == 200:
                        self.proxies.append(proxy_host)
                except:
                    pass
            page += 1

if __name__ == '__main__':
    a = Proxies()
    print(a.proxies)
    proxie = a.proxies
    with open('proxies.txt', 'w') as f:
        for proxy in proxie:
            f.write(proxy+'\n')
