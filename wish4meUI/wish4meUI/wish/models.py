#! -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from wish4meUI.wishlist.models import Wishlist

import random
import string
import os

# Create your models here.

class Wish(models.Model):
  wish_for = models.ForeignKey(User)
  description = models.TextField()
  category = models.ForeignKey('WishCategory')
  related_list = models.ForeignKey(Wishlist)

  brand = models.CharField(max_length=100)
  name = models.CharField(max_length=100)

  request_date = models.DateTimeField(auto_now=True, auto_now_add=True)
  is_accomplished = models.BooleanField(default=False)
  accomplish_date = models.DateTimeField(blank=True, null=True)

  #location =
  is_hidden = models.BooleanField(default = False)
  is_private = models.BooleanField(default = False)


  def __unicode__(self):
    return '%s %s' % (self.related_list.owner, self.description)

  def getPhotos(self):
    if hasattr(self, '_photos'):
      return self._photos
    else:
      self._photos = WishPhoto.objects.filter(wish=self)
    return self._photos


class WishCategory(models.Model):

  parent = models.ForeignKey('WishCategory', blank=True, null=True)
  name = models.CharField(max_length=100)
  synonyms = models.CharField(max_length=1000, blank=True, null=True)
  is_approved = models.BooleanField(default=True)
  is_hidden = models.BooleanField(default = False)

  #icon

  def __unicode__(self):
    return self.name

class _WishPhoto(models.Model):
  photo = models.ImageField(upload_to="photos/%s/" %
''.join(random.choice(string.letters + string.digits) for x in range(int(random.random()*35))), blank=True, null=True)

  is_hidden = models.BooleanField(default = False)

  def save(self):
    if not self.is_hidden:
      super(_WishPhoto,self).save()
      old_path = os.path.split(self.photo.file.name)[0]
      extension =  os.path.splitext(self.photo.file.name)[-1]
      new_name = "%s%s" % (''.join(random.choice(string.letters + string.digits) for x in range(int(random.random()*35))), extension)
      os.rename(self.photo.file.name, old_path+"/"+new_name)

      old_url_head = os.path.split(self.photo.url)[0]

      self.photo.name = "photos" +  old_path[old_path.rfind('/'):] + "/" + new_name
    super(_WishPhoto, self).save()

  def __unicode__(self):
    return self.photo.file.name

  class Meta:
    abstract = True

class WishPhoto(_WishPhoto):
  wish = models.ForeignKey("Wish")

ACCOMPLISH_STATUS = (
    ("1", "Sent"),
    ("2", "Accepted"),
    ("3", "Declined")
)


class WishAccomplish(models.Model):
  wish = models.ForeignKey("Wish")
  accomplisher = models.ForeignKey(User, related_name="accomplisher")
  description = models.TextField()
  status = models.CharField(max_length=1, choices=ACCOMPLISH_STATUS, default="1")
  response = models.TextField(blank=True, null=True)

class WishAccomplishPhoto(_WishPhoto):
  accomplish = models.ForeignKey("WishAccomplish")
