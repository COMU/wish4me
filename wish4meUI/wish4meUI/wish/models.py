#! -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import random
import string
import os

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

class WishPhoto(models.Model):
  wish = models.ForeignKey("Wish")
  photo = models.ImageField(upload_to="photos/%s/" % ''.join(random.choice(string.letters + string.digits) for x in range(int(random.random()*35))))

  is_hidden = models.BooleanField(default = False)

  def save(self):
    if not self.is_hidden:
      super(WishPhoto,self).save()
      old_path = os.path.split(self.photo.file.name)[0]
      extension =  os.path.splitext(self.photo.file.name)[-1]
      new_name = "%s%s" % (''.join(random.choice(string.letters + string.digits) for x in range(int(random.random()*35))), extension)
      os.rename(self.photo.file.name, old_path+"/"+new_name)

      old_url_head = os.path.split(self.photo.url)[0]

      self.photo.name = "photos" +  old_path[old_path.rfind('/'):] + "/" + new_name 
    super(WishPhoto, self).save()

  def __unicode__(self):
    return self.photo.file.name
