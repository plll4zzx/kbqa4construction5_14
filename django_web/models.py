# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserModel(models.Model):   #创建userModel表  用户表
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __unicode__(self):
        return self.username