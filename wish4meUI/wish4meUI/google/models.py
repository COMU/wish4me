#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class GoogleProfile(models.Model):
  user = models.ForeignKey(User)
  email = models.CharField(max_length=100)
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)

  def __unicode__(self):
    return self.email
