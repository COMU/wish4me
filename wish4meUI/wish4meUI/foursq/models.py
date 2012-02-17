from django.db import models

from wish4meUI.auth.models import LoginProfile
from wish4meUI.foursq.backend import FoursqBackend

class FoursqProfile(LoginProfile):

    foursq_id = models.IntegerField()
    access_token = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    def getLoginBackend(self, request):
        print "getLoginBackend called"
        return FoursqBackend(self, request)

    def __unicode__(self):
        return self.email

#class Foursq_Friend(models.Model):
#    foursq_id = models.IntegerField()
#    foursq_user = models.ManyToManyField(Foursq_User)

