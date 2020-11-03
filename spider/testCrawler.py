#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup as btsoup
import re

url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
cookie = 'Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1555855492; JSESSIONID=8BFEA0DFEE27F406084A02AE9B095F49; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1555855504'.decode("gbk").encode("utf-8")
host = "jzsc.mohurd.gov.cn"
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
addr = u'河北省'
pg = 6
headers = {
    "cookie": cookie,
    "host": host,
    "user-agent": userAgent
}
data = {
    'apt_code': '',
    'qy_fr_name': '',
    '$total': '11973',
    'qy_reg_addr': '%E6%B2%B3%E5%8C%97%E7%9C%81',
    'qy_code': '',
    'qy_name': '',
    '$pgsz': '15',
    'apt_certno': '',
    'qy_region': '130000',
    '%24reload': '0',
    'qy_type': '',
    '$pg': pg,
    'qy_gljg': '',
    'apt_scope': ''
}
response = requests.post(url, headers=headers, data=data)
pageD = btsoup(response.text, 'lxml')
list_ = []
patternT = re.compile(ur'\S{1,}')
for data['$pg'] in range(1, 7):
    for pp in pageD.find_all('td'):
        try:
            if pp.attrs['data-header'] == u'统一社会信用代码':
                try:
                    list_.append(patternT.search(pp.contents[0]).group())
                except:
                    list_.append(' ')
        except:
            continue

for li in list_:
    print li
'''
for idx, para in enumerate(patternT.findall(textAll.text)):
	list_.append(para)


		if ppp[0] == 'text-left' and ppp[1] == 'complist-num':
			print patternT.search(pp.contents[0]).group()

patternT = re.compile(ur'\S{1,}')
list_=[]
patternAll=re.compile(ur'tbody')
textAll=pageD.find(patternAll)
patternCh=re.compile(ur'[\u4e00-\u9fa5]{1,}')
str_=textAll.contents[1].text
ppp=patternCh.search(str)
print ppp

'''
