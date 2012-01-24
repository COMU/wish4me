#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.db import models

from wish4meUI.auth.models import LoginProfile
from wish4meUI.google.backend import GoogleBackend


class GoogleProfile(LoginProfile):

  email = models.CharField(max_length=100)
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)

  def getLoginBackend(self, request):
    return GoogleBackend(self, request)

  def __unicode__(self):
    return self.email
