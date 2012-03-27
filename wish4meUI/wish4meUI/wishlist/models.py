from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wishlist(models.Model):
  owner = models.ForeignKey(User, related_name="owner")
  title = models.CharField(max_length=140)
  is_private = models.BooleanField(default = False)
  is_hidden = models.BooleanField(default = False)

  def __unicode__(self):
    return '%s' % (self.title)
