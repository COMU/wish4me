#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from wish4meUI.auth.models import LoginProfile
from wish4meUI.twitter_app.backend import TwitterBackend


class TwitterProfile(LoginProfile):

  twitter_id = models.IntegerField(unique = True)
  screenname = models.CharField(max_length=100)
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)

  def getLoginBackend(self, request):
      return TwitterBackend(self, request)

  def __unicode__(self):
    return self.screen_name
