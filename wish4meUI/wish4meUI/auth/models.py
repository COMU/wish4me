#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models


class LoginProfile(models.Model):
  is_logged_in = models.BooleanField()

  class Meta:
    abstract =True

  def getUserProfile(self):
    return self.userprofile_set
