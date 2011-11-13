from django.db import models
from django.contrib.auth.models import User


class Foursq_User(models.Model):
    foursq_id = models.IntegerField()
    user = models.OneToOneField(User)

class Foursq_Friend(models.Model):
    foursq_id = models.IntegerField()
    foursq_user = models.ManyToManyField(Foursq_User)

