#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class FriendshipManager(models.Manager):

  def areFriends(self, user_1, user_2):
    if self.filter(from_user=user_1, to_user=user_2, is_hidden= False).count() > 0:
      if self.filter(from_user=user_2, to_user=user_1, is_hidden= False).count() > 0:
        return True
    return False
  
  def remove(self, user_1, user_2):
    friendship_to_end = self.filter(from_user=user_1, to_user=user_2, is_hidden= False)
    if friendship_to_end:
      friendship_to_end.is_Hidden = True
      friendship_to_end.hide_date = datetime.now()
      friendship_to_end.save()

class Friendship(models.Model):

  from_user = models.ForeignKey(User, related_name="friends_with")
  to_user = models.ForeignKey(User, related_name="friend_of")
  date_created = models.DateTimeField("date_created", default=datetime.now())
  is_hidden = models.BooleanField("Hiddden", default=False)
  hide_date = models.DateTimeField("hide_date", blank=True)

  class Meta:
    unique_together = (('to_user', 'from_user'),)

def friendSetFor(user):
  return set([obj["friend"] for obj in Friendship.objects.friends_for_user(user)])

INVITE_STATUS = (
    ("1", "Sent"),
    ("2", "Expired"),
    ("3", "Accepted"),
    ("4", "Declined"),
    ("5", "Deleted")
)

class FriendshipInvitation(models.Model):
  from_user = models.ForeignKey(User, related_name="invitations_from")
  to_user = models.ForeignKey(User, related_name="invitations_to")
  message = models.TextField( blank = True)
  status = models.CharField(max_length=1, choices=INVITE_STATUS, default="1")
  date_created = models.DateTimeField("date_created", default=datetime.now())
  
  def accept(self):
    # mark invitation accepted
    self.status = "3"
    self.save()
    # auto-create friendship
    friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
    friendship.save()

  def decline(self):
    if not Friendship.objects.are_friends(self.to_user, self.from_user):
      self.status = "4"
      self.save()

  def __unicode__(self):
    return self.from_user +" to " + self.to_user +" invite"
