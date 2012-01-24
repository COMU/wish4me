#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)

  last_login_backend_name = models.CharField(max_length=100,
                                             blank=True, null=True)

  google_profile = models.OneToOneField(
      'google.GoogleProfile',
      blank=True, null=True, related_name='userprofile_set')
  facebook_profile = models.OneToOneField(
      'facebook.FacebookProfile',
      blank=True, null=True, related_name='userprofile_set')
  twitter_profile = models.OneToOneField(
      'twitter_app.TwitterProfile',
      blank=True, null=True, related_name='userprofile_set')

  def __unicode__(self):
    return self.user.__unicode__()
