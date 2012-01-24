#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from wish4meUI.userprofile.models import UserProfile


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
      except UserProfile.DoesNotExist:
        user = User(**user_kwargs)
        user.save()
        kwargs = {related_name: profile}
        userprofile = UserProfile(user=user, **kwargs)
        userprofile.last_login_backend_name = related_name
        userprofile.save()

      return userprofile.user
