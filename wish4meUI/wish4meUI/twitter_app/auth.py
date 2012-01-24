#!/usr/bin/python
# -*- coding: utf-8 -*-

from openid.consumer.consumer import SUCCESS

from django.contrib.auth.models import User
from django.core.mail import mail_admins

from wish4meUI.google.models import GoogleProfile
from wish4meUI.userprofile.models import UserProfile
from wish4meUI.twitter_app.models import TwitterProfile
import settings


class TwitterAuthBackend(object):
  def authenticate(self, request, credentials):

    if credentials is None:
      return None

    twitter_id = credentials['id']
    twitter_screenname = credentials['screen_name']
    twitter_username = credentials['name']


    try:
      twitter_profile = TwitterProfile.objects.get(twitter_id=twitter_id)

    except TwitterProfile.DoesNotExist:
      twitter_profile = TwitterProfile(
          twitter_id = twitter_id,
          screenname = twitter_screenname,
          firstname = twitter_username.rsplit()[0],
          lastname = twitter_username.rsplit()[1])

    twitter_profile.save()
    backend = twitter_profile.getLoginBackend(request)
    print "user edek basgan"
    user = backend.login(
        twitter_profile, related_name='twitter_profile',
        username=twitter_screenname, email=settings.DEFAULT_EMAIL)
    print "user olusturduk"
    return user


  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
