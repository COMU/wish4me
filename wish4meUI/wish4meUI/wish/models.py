from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wish(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(WishCategory, help_text="Category that the wish belongs to")
    subcategory = models.ForeignKey(WishSubCategory, help_text="Sub category that the wish belongs to")
    to_who = models.ForeignKey(User)
    request_date = models.DateTimeField(auto_now=True)
    accomplish_date = models.DateTimeField(blank=True)
    #location =

class WishCategory(models.Model):
    name = models.CharField(max_length=100)

class WishSubCategory(models.Model):
    name = models.CharField(max_length=100)

