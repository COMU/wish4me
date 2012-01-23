#!/usr/bin/python
# -*- coding: utf-8 -*-

from openid.consumer.consumer import SUCCESS

from django.contrib.auth.models import User
from django.core.mail import mail_admins

from wish4meUI.google.models import GoogleProfile
from wish4meUI.userprofile.models import UserProfile


class GoogleAuthBackend(object):

  def authenticate(self, openid_response):

    if openid_response is None:
      return None
    if openid_response.status != SUCCESS:
      return None

    google_email = openid_response.getSigned(
        'http://openid.net/srv/ax/1.0', 'value.email')
    google_firstname = openid_response.getSigned(
        'http://openid.net/srv/ax/1.0', 'value.firstname')
    google_lastname = openid_response.getSigned(
        'http://openid.net/srv/ax/1.0', 'value.lastname')
    try:
      google_profile = GoogleProfile.objects.get(email=google_email)
      google_profile.last_login_backend_name = 'google'
      google_profile.save()
      user = google_profile.user
    except GoogleProfile.DoesNotExist:
      user = User(username=google_email, email=google_email)
      user.save()
      user_profile = UserProfile(
          user=user, last_login_backend_name='google')
      user_profile.save()
      google_profile = GoogleProfile(
          user=user,
          email=google_email,
          firstname=google_firstname,
          lastname=google_lastname)
      google_profile.save()
    return user

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
