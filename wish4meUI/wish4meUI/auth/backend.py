#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login as djangoLogin

from wish4meUI.userprofile.models import UserProfile
from django.conf import settings

class LoginBackend(object):
    """Provides a base class for all authentication
    backends for generic methods.
    """

    def __init__(self, _profile, request):
        self._request = request
        self._login_profile = _profile

    def postMessage(self):
        """Post a message on user's profile.
        """
        raise NotImplementedError

    def getProfilePicture(self):
        """Fetch profile picture of user.
        """
        raise NotImplementedError

    def getFriends(self):
        """Return friends within wish4me.
        """
        raise NotImplementedError

    def logout(self):
        pass

    def login(self, profile, related_name, **user_kwargs):

      try:
        userprofile = profile.getUserProfile()
        user = userprofile.user
      except UserProfile.DoesNotExist:
        user = User(**user_kwargs)
        user.password = settings.DEFAULT_PASSWORD
        user.save()
        kwargs = {related_name: profile}
        userprofile = UserProfile(user=user, **kwargs)
        userprofile.last_login_backend_name = related_name
        userprofile.save()
      #djangoLogin(self._request,user)

      return userprofile.user
