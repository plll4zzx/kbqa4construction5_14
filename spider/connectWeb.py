#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import requests
import pymysql
import math
from bs4 import BeautifulSoup as btsoup
import json
import random
from goto import *

class connectWeb:
	def __init__(self):
		self.proxyOrNot=0	#1 means use
		self.proxyPayOrNot=1 #1 means in pay

		self.url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/{catg}/{url4comp}'
		self.cookie = 'Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1555855492; JSESSIONID=8BFEA0DFEE27F406084A02AE9B095F49; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1555855504'.decode(
			'gbk').encode('utf-8')
		self.host = 'jzsc.mohurd.gov.cn'
		self.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"

		self.headers = {
			"cookie": self.cookie,
			"host": self.host,
			"user-agent": self.userAgent
		}
		pg=1
		self.data={
			'$total':'',
			'$reload':'',
			'$pg':pg ,
			'$pgsz':25
		}

		dbFormal = "kg4company_2"
		dbTest = 'kg_test'
		self.db = pymysql.connect("localhost", "root", "root", dbTest, charset="utf8")
		#self.db = pymysql.connect("localhost", "root", "root", "kg_test", charset="utf8")
		self.ipNum=0
		self.ipList=[]
		self.ipFlag=[]
		self.ipLoc=[]
		self.proxies = {
			"http": '',
			"https": '',
		}

	def setIpList(self):
		print ''

	def getIp(self):
		if self.ipNum>=10:
			self.setIpList()
		return self.ipList[self.ipNum]

	def _del_(self):
		self.db.close()

	def setProxy(self):
		if self.proxyPayOrNot:
			proxyMeta=self.getIp()
		else:
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

		self.proxies = {
			"http": proxyMeta,
			"https": proxyMeta,
		}

	def getResponse(self,flag):
		if flag:
			if self.proxyOrNot:
				self.setProxy()
				response = requests.post(self.url, headers=self.headers,proxies=self.proxies)
			else:
				response = requests.post(self.url, headers=self.headers)
		else:
			if self.proxyOrNot:
				self.setProxy()
				response = requests.post(self.url, headers=self.headers, data=self.data, proxies=self.proxies)
			else:
				response = requests.post(self.url, headers=self.headers, data=self.data)
		return response

	def getHtml(self, catg, url4comp, flag=1): #flag：Get next page or not

		#proxy
		self.url = self.url.format(catg=catg, url4comp=url4comp)
		count=0
		while count<3:
			soup = btsoup(self.getResponse(flag).text, 'html.parser')
			try:
				if soup.contents[0].contents[1].contents[0].text[0]=='5':
					count=count+1
					print('504! Wait and try No.'+str(count))
					time.sleep(count)	#when network is busy wait and try again
				else:
					break
			except:
				break
		return soup

	def insert2sql(self, sql):
		cur = self.db.cursor()
		reCount = cur.execute(sql)  # 返回受影响的行数
		self.db.commit()
		print(reCount)

class compInfo(connectWeb):
	def getInfo(self, url4comp):
		catg = 'compDetail'
		flag=0
		while flag<3:
			pageD = self.getHtml(catg, url4comp)
			if pageD.contents[0][0]=='5':
				flag=flag+1
				print('504 '+str(flag))
			else:
				break
		patternT = re.compile(ur'\S{1,}')
		list_ = [' ',' ',' ',' ',' ',' ']
		for pp in pageD.find_all('div'):
			try:
				ppp = pp.attrs['class']
				if ppp[0] == 'user_info' and ppp[1] == 'spmtop':
					list_[0]=patternT.search(pp.contents[1].contents[1]).group()
			except:
				pass
		listTag = [u"统一社会信用代码", u"企业法定代表人", u"企业登记注册类型", u"企业注册属地", u"企业经营地址"]
		sql = u"INSERT INTO compInfo(name_, uscc, legalRpst, category, province, adrs) VALUES ('{name_}', '{uscc}', '{legalRpst}', '{category}', '{province}', '{adrs}');"
		for pp in pageD.find_all('td'):
			try:
				for idx, lt in enumerate(listTag):
					try:
						if pp.attrs['data-header'] == lt:
							try:
								list_[idx+1]=patternT.search(pp.contents[0]).group()
								if idx==4:
									sql1 = sql.format(name_=list_[0], uscc=list_[1], legalRpst=list_[2], category=list_[3], province=list_[4],adrs=list_[5])
									print sql1
									self.insert2sql(sql1)
									break
							except:
								pass
					except:
						pass
			except:
				pass
		return list_[0]

class compAptitude(connectWeb):
	def getInfo(self, url4comp, compName):
		catg='caDetailList'
		pageD = self.getHtml(catg, url4comp)
		patternT = re.compile(ur'\S{1,}')
		list_ = [' ', ' ', ' ', ' ', ' ', ' ',' ']
		listTag = [u"序号", u"资质类别", u"资质证书号", u"资质名称", u"发证日期",u"证书有效期",u"发证机关"]
		sql = u"INSERT INTO compAptitude(No_, category, id, name_, fromWhen, toWhen, fromWhere, compName) VALUES ('{No}', '{category}', '{id}', '{name}', '{fromWhen}', '{toWhen}', '{fromWhere}', '{compName}');"
		for pp in pageD.find_all('td'):
			try:
				for idx, lt in enumerate(listTag):
					try:
						if pp.attrs['data-header'] == lt:
							try:
								list_[idx] = patternT.search(pp.contents[0]).group()
								if idx==6:
									sql1 = sql.format(No=list_[0], category=list_[1], id=list_[2], name=list_[3],
													  fromWhen=list_[4], toWhen=list_[5],
													  fromWhere=list_[6], compName=compName)
									list_ = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
									print sql1
									self.insert2sql(sql1)
							except:
								pass
					except:
						pass
			except:
				pass

class peopleInfo(connectWeb):
	def getInfo(self, url4comp, compName, page_n=1):
		catg='regStaffList'
		self.data['$pg']=page_n
		pageD = self.getHtml(catg, url4comp,flag=0)
		patternT = re.compile(ur'\S{1,}')
		list_ = [' ', ' ', ' ', ' ', ' ', ' ']
		listTag = [u"序号", u"姓名", u"身份证号", u"注册类别", u"注册号（执业印章号）",u"注册专业"]
		sql = u"INSERT INTO peopleInfo(No_, name_, id_p, category, id_reg, major, compName) VALUES ('{No}', '{name}', '{id_p}', '{category}', '{id_reg}', '{major}', '{compName}');"
		flag=0
		numP=0
		for pp in pageD.find_all('td'):
			try:
				for idx, lt in enumerate(listTag):
					try:
						if pp.attrs['data-header'] == lt:
							try:
								if idx==1:
									list_[idx] = patternT.search(pp.contents[1].contents[0]).group()
								else:
									list_[idx] = patternT.search(pp.contents[0]).group()
								if idx==5:
									sql1 = sql.format(No=list_[0],  name=list_[1], id_p=list_[2], category=list_[3],
													  id_reg=list_[4], major=list_[5], compName=compName)
									list_ = [' ', ' ', ' ', ' ', ' ', ' ']
									numP = numP + 1
									print sql1
									print numP
									self.insert2sql(sql1)
							except:
								flag=1
								numLi=0
								for li in list_:
									if li!=' ':
										numLi=numLi+1
								if numLi>=3:
									sql1 = sql.format(No=list_[0], name=list_[1], id_p=list_[2], category=list_[3],
													  id_reg=list_[4], major=list_[5], compName=compName)
									list_ = [' ', ' ', ' ', ' ', ' ', ' ']
									numP = numP + 1
									print sql1
									print numP
									self.insert2sql(sql1)
									flag=0
								pass
					except:
						flag=1
						pass
			except:
				flag=1
				pass
		if numP%25==0 and numP>0:
			flag=0
		return flag

class projectInfo(connectWeb):
	def getInfo(self, url4comp, compName, page_n=1):
		self.data['$pg']=page_n
		catg='compPerformanceListSys'
		pageD = self.getHtml(catg, url4comp,flag=0)
		patternT = re.compile(ur'\S{1,}')
		list_ = [' ', ' ', ' ', ' ', ' ', ' ']
		listTag = [u"序号", u"项目编码", u"项目名称", u"项目属地", u"项目类别",u"建设单位"]
		sql = u"INSERT INTO projectInfo(No_, id, name_, where_, category, whom_, compName) VALUES ('{No}', '{id}', '{name}', '{where}', '{category}', '{whom}', '{compName}');"
		flag=0
		numP=0
		for pp in pageD.find_all('td'):
			try:
				for idx, lt in enumerate(listTag):
					try:
						if pp.attrs['data-header'] == lt:
							try:
								if idx==2:
									list_[idx] = patternT.search(pp.contents[0].contents[0]).group()
								else:
									list_[idx] = patternT.search(pp.contents[0]).group()
								if idx==5:
									sql1 = sql.format(No=list_[0], id=list_[1], name=list_[2], where=list_[3],
								  			category=list_[4], whom=list_[5], compName=compName)
									list_ = [' ', ' ', ' ', ' ', ' ', ' ']
									numP = numP + 1
									print sql1
									print numP
									self.insert2sql(sql1)
							except:
								flag=1
								numLi=0
								for li in list_:
									if li!=' ':
										numLi=numLi+1
								if numLi>=3:
									sql1 = sql.format(No=list_[0], id=list_[1], name=list_[2], where=list_[3],
													  category=list_[4], whom=list_[5], compName=compName)
									list_ = [' ', ' ', ' ', ' ', ' ', ' ']
									numP = numP + 1
									print sql1
									print numP
									self.insert2sql(sql1)
									flag=0
								pass
					except:
						flag = 1
						pass
			except:
				flag = 1
				pass
		if numP%25==0 and numP>0:
			flag=0
		return flag
if __name__=='__main__':
	cf=compInfo()
	cf2=projectInfo()
	cf3=peopleInfo()
	cf4=compAptitude()
	str1=u'001607220057324528'
	strr= cf.getInfo(str1)

	page=1
	while 1:
		if cf2.getInfo(str1,strr,page_n=page):
			break
		page=page+1

	page=1
	while 1:
		if cf3.getInfo(str1,strr,page_n=page):
			break
		page=page+1

	cf4.getInfo(str1,strr)
