from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	TwitterID = models.IntegerField('TwitterID', unique=True, blank=True, null=True,)
	TwitterToken = models.CharField('TwitterAccessToken', blank=True, null=True, max_length = 100)
	FoursquareID = models.IntegerField('FoursquareID', unique=True, blank=True, null=True)
	FoursquareToken = models.CharField('FoursquareToken', blank=True, null=True, max_length = 100)
