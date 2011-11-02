from django.db import models
from django.contrib.auth.models import User

class Foursq_User(models.Model):
    foursq_id = models.IntegerField()
    user = models.ForeignKey(User)
