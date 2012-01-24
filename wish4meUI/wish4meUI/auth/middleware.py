#!/usr/bin/python
# -*- coding: utf-8 -*-


class LoginMiddleware(object):

  def process_request(self, request):
    if not request.user.is_authenticated() or request.path.startswith('/admin/'):
      request.profile = None
      request.login_backend = None
      request.last_login_profile = None
    else:
      request.profile = request.user.get_profile()
      last_login_profile_name = request.user.profile.last_login_profile_name
      request.last_login_profile = getattr(request.profile, last_login_profile_name)
