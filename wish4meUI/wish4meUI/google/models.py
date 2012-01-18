#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

from wish4meUI.userprofile.models import UserProfile


class GoogleProfile(models.Model):
  user_profile = models.ForeignKey(UserProfile)
  email = models.CharField(max_length=100)
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)

  def __unicode__(self):
    return self.email
