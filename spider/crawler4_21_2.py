#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import requests
import urllib2
from bs4 import BeautifulSoup as btsoup
import connectWeb
import Crawler as cw
import threading
import pymysql
import time

def spider_thread(city):
	iii=0
	for idx in range(1, 30):
		cwler = cw.Crawler()
		cwler.getCompUrl(idx,city)
		list_=cwler.listComp
		print list_
		for li in list_:
			iii=iii+1
			print city+' company:'+str(iii)
			ci = connectWeb.compInfo()
			pri = connectWeb.projectInfo()
			pei = connectWeb.peopleInfo()
			ca= connectWeb.compAptitude()
			str4comp=ci.getInfo(li)
			pri.getInfo(li,str4comp)
			pei.getInfo(li,str4comp)
			ca.getInfo(li,str4comp)
			time.sleep(3)
			print city+' This company is done, take a rest'
		time.sleep(5)
		print city+' This page is done, take a rest'


db = pymysql.connect("localhost","root","root","kg4company_2", charset="utf8")
cur = db.cursor()

sql1 = u"select name from city;"
reCount = cur.execute(sql1)  # 返回受影响的行数
cities = cur.fetchall()
cities=cities[3:len(cities)-1]
for city in cities:
	print city[0]
	''''''
	spider_thread(city[0])
	print city[0]+'is done, wait a minute and take a rest'
	time.sleep(5)
