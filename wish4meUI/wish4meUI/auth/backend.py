#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as djangoLogin
from django.db import models

from wish4meUI.userprofile.models import UserProfile
from wish4meUI.wishlist.views import addDefaultWishlist
from wish4meUI.wish.models import Wish
from django.conf import settings


def mergeAccounts(merge_into_user, merge_from_user):
  """
  """
  
  #All models and fields related to merge_from_user
  for Model in models.get_models():
    
    if Model == UserProfile:
      continue
    
    for field in Model._meta.fields:
      if type(field) == models.ForeignKey:
        if field.related.parent_model == User:
          search = {field.name: merge_from_user}
          objects = Model.objects.filter(**search)
          for obj in objects:
            setattr(obj, field.name, merge_into_user)
            obj.save()
  
  # Delete old profile
  merge_from_profile = merge_from_user.get_profile()
  merge_into_profile = merge_into_user.get_profile()
  
  if merge_from_profile.google_profile:
    merge_into_profile.google_profile = merge_from_profile.google_profile
    
  if merge_from_profile.facebook_profile:
    merge_into_profile.facebook_profile = merge_from_profile.facebook_profile
    
  if merge_from_profile.twitter_profile:
    merge_into_profile.twitter_profile = merge_from_profile.twitter_profile

  if merge_from_profile.foursq_profile:
    merge_into_profile.foursq_profile = merge_from_profile.foursq_profile
  
  merge_into_profile.save()
  
  merge_from_profile.delete()
  merge_from_user.delete()
  
          

  
  
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
          user = userprofile.user #
          if already_logged_user:
            merge_from_user = user
            merge_into_user = already_logged_user
          
            mergeAccounts(merge_into_user, merge_from_user)
            user = already_logged_user
            
            messages.add_message(self._request, messages.SUCCESS,
                                 "Account you were trying to activate "
                                 "already existed. Merged it into this "
                                 "account. ")
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
