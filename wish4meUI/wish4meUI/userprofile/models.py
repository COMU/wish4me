from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	TwitterID = models.IntegerField('TwitterID', unique=True, blank=True)
	TwitterToken = models.CharField('TwitterAccessToken', blank=True, max_length = 100)
