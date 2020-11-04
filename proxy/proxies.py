# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import http.client
import threading

inFile = 0
outFile = 0
lock = threading.Lock()

def getProxyList(targeturl="http://www.66ip.cn/"):
    countNum = 0
    proxyFile = open('proxy_1.txt' , 'w')
    
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

    for page in range(1, 1024):
        url = targeturl + str(page) + '.html'
        #print url
        req = requests.get(url, headers=requestHeader)
        html_doc = req.text
    
        soup = BeautifulSoup(html_doc, "html.parser")
        #print soup
        
        ip_list = soup.find_all("table")
        if len(ip_list) < 1:
                continue
        
        trs = ip_list[-1].find_all("tr")
        for tr in trs[1:]:
            tds = tr.find_all('td')
            
            if len(tds) < 1:
                    continue
            # #国家
            # if tds[0].find('img') is None :
            #     nation = '未知'
            #     locate = '未知'
            # else:
            #     nation =   tds[0].find('img')['alt'].strip()
            #     locate  =   tds[3].text.strip()
            ip      =   tds[0].text.strip()
            port    =   tds[1].text.strip()
            locate  =   tds[2].text.strip()
            anony   =   tds[3].text.strip()
            # protocol=   tds[5].text.strip()
            # speed   =   tds[6].find('div')['title'].strip()
            time    =   tds[4].text.strip()
            
            proxyFile.write('%s|%s|%s|%s|%s\n' % (ip, port, locate, anony, time) )
            print ('%s://%s:%s' % (anony, ip, port))
            countNum += 1
    
    proxyFile.close()
    return countNum
    
def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'https://comment.bilibili.com/125463156.xml'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.split('|')
        protocol= 'https'
        ip      = line[0]
        port    = line[1]
        
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method = 'GET', url = myurl, headers = requestHeader )
            res = conn.getresponse()
            tmp = res.read()
            conn.close()
            if b'"code":-412' in tmp:
                print ("---Reject :" + ip + ":" + port)
                continue
            lock.acquire()
            print ("+++Success:" + ip + ":" + port)
            outFile.write(ip + ":" + port + "\n")
            lock.release()
        except:
            print ("---Failure:" + ip + ":" + port)
        
    
if __name__ == '__main__':
    # tmp = open('proxy.txt' , 'w')
    # tmp.write("")
    # tmp.close()

    proxynum = getProxyList("http://www.66ip.cn/")
    # print (u"国内高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/nt/")
    # print (u"国内透明：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print (u"国外高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print (u"国外透明：" + str(proxynum))

    print (u"\n验证代理的有效性：")
    
    inFile = open('proxy_1.txt', 'r')
    outFile = open('verified_1.txt', 'w')
    
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
        
    for t in all_thread:
        t.join()
    
    inFile.close()
    outFile.close()
    print ("All Done.")