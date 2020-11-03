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

def storeUrl4Comp():
	db = pymysql.connect("localhost","root","root","kg4company_2", charset="utf8")
	cur = db.cursor()
	sql1 = u"select name from city;"
	reCount = cur.execute(sql1)  # 返回受影响的行数
	cities1 = cur.fetchall()
	sql2 = u"select name from industry;"
	cur.execute(sql2)
	cities2=cur.fetchall()
	cities=cities1+cities2
	sql3=u"insert into urlList(url4comp) values('{name}');"
	cities=cities[71:]
	for city in cities:
		print city[0]
		for idx in range(1, 31):
			print('page: '+str(idx))
			cwler = cw.Crawler()
			cwler.getCompUrl(idx, city[0])
			list_ = cwler.listComp
			if len(list_)==0:
				break
			for li in list_:
				print li
				sqlN=sql3.format(name=li)
				cur.execute(sqlN)
				db.commit()
			time.sleep(2)
			print('page: '+str(idx)+' is done')
		time.sleep(2)
		print(city[0]+' is done')

def getUrl4comp():
	dbFormal="kg4company_2"
	dbTest='kg_test'
	db = pymysql.connect("localhost","root","root",dbFormal, charset="utf8")
	cur = db.cursor()
	sqlAll=u'select url4comp from urlList group by url4comp'
	cur.execute(sqlAll)
	url4comp=cur.fetchall()
	list_=[]
	for url in url4comp:
		list_.append(url[0])
	return list_

def crawler(num_s,num_e):
	list_1=getUrl4comp()
	#list_1=list_1[1:3]
	for idx, li1 in enumerate(list_1[num_s:num_e]):
		print('company No.'+str(idx+num_s)+' : '+li1)
		ci = connectWeb.compInfo()
		pri = connectWeb.projectInfo()
		pei = connectWeb.peopleInfo()
		ca= connectWeb.compAptitude()
		str4comp=ci.getInfo(li1)
		time.sleep(1)
		page = 1
		while 1:
			if pri.getInfo(li1,str4comp,page_n=page):
				break
			page = page + 1
			time.sleep(1)
		page = 1
		while 1:
			if pei.getInfo(li1,str4comp,page_n=page):
				break
			page = page + 1
			time.sleep(1)

		ca.getInfo(li1,str4comp)
		print('company '+str4comp+' is done')
		time.sleep(2)

crawler(1,4)

