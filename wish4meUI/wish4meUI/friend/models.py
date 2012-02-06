#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class FollowingManager(models.Manager):

  def areFriends(self, user_1, user_2):
    if self.filter(from_user=user_1, to_user=user_2, is_hidden= False).count() > 0:
      if self.filter(from_user=user_2, to_user=user_1, is_hidden= False).count() > 0:
        return True
    return False

  def remove(self, user_1, user_2):
    following_to_end = self.filter(from_user=user_1, to_user=user_2, is_hidden= False)
    if friendship_to_end:
      friendship_to_end.is_Hidden = True
      friendship_to_end.hide_date = datetime.now()
      friendship_to_end.save()


class Following(models.Model):

  from_user = models.ForeignKey(User, related_name="follower")
  to_user = models.ForeignKey(User, related_name="following")
  date_created = models.DateTimeField("date_created", default=datetime.now())
  is_hidden = models.BooleanField("Hiddden", default=False)
  hide_date = models.DateTimeField("hide_date", default=datetime.now())   # since this never used if not is_hidden.

  objects = FollowingManager()
  def save(self):
    if Following.objects.filter(from_user=self.from_user, to_user=self.to_user, is_hidden= False).count() > 0:
      pass
    else:
      pass #TODO(orcuna): create notification
    super(Following, self).save()

  class Meta:
    unique_together = (('to_user', 'from_user'),)
