# !/usr/bin/python
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

response = requests.post(self.url, headers=self.headers, data=self.data, proxies=proxies)
