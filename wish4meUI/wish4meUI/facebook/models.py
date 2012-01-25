#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from wish4meUI.auth.models import LoginProfile
from wish4meUI.facebook.backend import FacebookBackend


class FacebookProfile(LoginProfile):

    #user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def getLoginBackend(self, request):
      return FacebookBackend(self, request)

    def get_facebook_profile(self):
      fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
      return json.load(fb_profile)


class FacebookNewsFeed(models.Model):
    message =  models.CharField(max_length=420)
    facebook_id = models.BigIntegerField()
    date = models.DateField(auto_now=True)
    facebook_pub = models.IntegerField()

admin.site.register(FacebookProfile)
