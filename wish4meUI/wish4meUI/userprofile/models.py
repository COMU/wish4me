#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)

  last_login_backend_name = models.CharField(max_length=100)

  def __unicode__(self):
    return self.user.__unicode__()
