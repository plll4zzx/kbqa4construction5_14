#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import requests
from bs4 import BeautifulSoup as btsoup
import random
import json

class Crawler:
    def __init__(self):
        self.url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
        self.cookie = 'JSESSIONID=87C5302F887C894D411C5FD2FDF361A2; Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1555855492,1555933444,1556002757,1556024481; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1556024481'.decode(
            "gbk").encode("utf-8")
        self.host = "jzsc.mohurd.gov.cn"
        self.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        self.addr = u'河北省'
        pg = 1
        self.headers = {
            "cookie": self.cookie,
            "host": self.host,
            "user-agent": self.userAgent
        }
        self.data = {
            'apt_code': '',
            'qy_fr_name': '',
            '$total': '11973',
            'qy_reg_addr': self.addr,#'%E6%B2%B3%E5%8C%97%E7%9C%81'
            'qy_code': '',
            'qy_name': '邯郸',
            '$pgsz': '15',
            'apt_certno': '',
            'qy_region': '130000',
            '%24reload': '0',
            'qy_type': '',
            '$pg': pg,
            'qy_gljg': '',
            'apt_scope': ''
        }
        self.listComp = []

    # connect Mysql

    # set HB
    def getCompUrl(self,page_n,city):
        self.data['$pg']=page_n
        self.data['qy_name']=city
        proxyHost = "http-proxy-t1.dobel.cn"
        proxyPort = "9180"

        # 账号密码
        proxyUser = "PLLLSPIDER5GACPLP40"
        proxyPass = "YaWqCmT6"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        #response = requests.post(self.url, headers=self.headers, data=self.data)
        #pageD = btsoup(response.text, 'lxml')
        flag = 0
        while flag < 3:
            response = requests.post(self.url, headers=self.headers, data=self.data, proxies=proxies)
            pageD = btsoup(response.text, 'lxml')
            try:
                if pageD.contents[0][0] == '5':
                    print('504 ' + str(flag))
                    flag = flag + 1
                else:
                    break
            except:
                flag = flag + 1
                pass
        patternT = re.compile(ur'\d{6,}')
        for pp in pageD.find_all('a'):
            try:
                self.listComp.append(patternT.search(pp.attrs['href']).group())
            except:
                pass

    def startWork(self):
        print 'qwe'


# company one by one

# page down
if __name__ == '__main__':
    for idx in range(1,2):
        cwler = Crawler()
        city=u'廊坊'
        cwler.getCompUrl(idx,city)
        for li in cwler.listComp:
            print li
