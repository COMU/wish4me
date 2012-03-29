#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as djangoLogin

from wish4meUI.userprofile.models import UserProfile
from wish4meUI.wishlist.views import addDefaultWishlist
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

      if self._request.user and self._request.user.is_authenticated():
        already_logged_user = self._request.user
      else:
        already_logged_user = None

      try:
          #if related_name == "foursq_profile":
          #    print "foursq_profile"
          #    profile = UserProfile.objects.get(foursq_profile=profile)
          #    print profile
          userprofile = profile.getUserProfile()
          user = userprofile.user
          if already_logged_user:
            messages.add_message(self._request, messages.ERROR,
                                 "This external account has already "
                                 "been used before. Merging profiles "
                                 "is not yet possible! Switched to "
                                 "this account now!")
      except UserProfile.DoesNotExist:
          if already_logged_user:
            user = already_logged_user
            userprofile = user.get_profile()
            setattr(userprofile, related_name, profile)
            userprofile.save()
            messages.add_message(self._request, messages.SUCCESS,
                                 "Activated new external account!")
          else:
            user = User(**user_kwargs)
            user.password = settings.DEFAULT_PASSWORD
            user.save()

            kwargs = {related_name: profile}
            userprofile = UserProfile(user=user, **kwargs)
            userprofile.last_login_backend_name = related_name
            userprofile.save()
            addDefaultWishlist(user)
      #djangoLogin(self._request,user)

      return user
