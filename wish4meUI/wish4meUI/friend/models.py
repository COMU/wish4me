#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Friendship(models.Model):

  from_user = models.ForeignKey(User, related_name="friends_with")
  to_user = models.ForeignKey(User, related_name="friend_of")
  date_created = models.DateTimeField("date_created", default=datetime.now())
  is_hidden = models.BooleanField("Hiddden", default=False)

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
  message = models.TextField()
  status = models.CharField(max_length=1, choices=INVITE_STATUS)
  date_created = models.DateTimeField("date_created", default=datetime.now())
  
  def accept(self):
    # mark invitation accepted
    self.status = "3"
    self.save()
    # auto-create friendship
    friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
    friendship.save()

  def __unicode__(self):
    return self.from_user +" to " + self.to_user " invate"
