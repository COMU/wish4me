#! -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wishlist(models.Model):
  owner = models.ForeignKey(User, related_name="owner")
  title = models.CharField(max_length=140)
  is_hidden = models.BooleanField(default = False)

class Wish(models.Model):
  wish_for = models.ForeignKey(User)
  description = models.TextField()
  category = models.ForeignKey('WishCategory')
  related_list = models.ForeignKey('Wishlist')

  brand = models.CharField(max_length=100)
  name = models.CharField(max_length=100)

  request_date = models.DateTimeField(auto_now=True, auto_now_add=True)
  accomplish_date = models.DateTimeField(blank=True, null=True)

  #photo =
  #location =
  is_hidden = models.BooleanField(default = False)

  def __unicode__(self):
    return '%s %s' % (self.related_list.owner, self.description)


class WishCategory(models.Model):

  parent = models.ForeignKey('WishCategory', blank=True, null=True)
  name = models.CharField(max_length=100)
  synonyms = models.CharField(max_length=1000, blank=True, null=True)
  is_approved = models.BooleanField(default=True)
  is_hidden = models.BooleanField(default = False)

  #icon

  def __unicode__(self):
    return self.name
