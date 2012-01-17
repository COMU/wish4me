#! -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wishlist(models.Model):
    owner = models.ForeignKey(User, related_name="owner")
    comment = models.CharField(max_length=140)

class Wish(models.Model):
    wish_for = models.ForeignKey(User)
    comment = models.CharField(max_length=140)
    category = models.ForeignKey('WishCategory')
    related_list = models.ForeignKey('Wishlist')

    request_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    accomplish_date = models.DateTimeField(blank=True, null=True)

    #photo =
    #location =

    def __unicode__(self):
      return '%s %s' % (self.related_list.owner, self.comment)


class WishCategory(models.Model):

    parent = models.ForeignKey('WishCategory', blank=True, null=True)
    name = models.CharField(max_length=100)
    synonyms = models.CharField(max_length=1000)
    is_approved = models.BooleanField(default=True)

    #icon

    def __unicode__(self):
      return self.name
