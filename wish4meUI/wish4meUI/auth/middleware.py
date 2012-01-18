#!/usr/bin/python
# -*- coding: utf-8 -*-

from wish4meUI.google.models import GoogleProfile

from wish4meUI.google.backend import GoogleBackend


LOGIN_MODULES = {
  'google': {'profile': GoogleProfile,
             'backend': GoogleBackend},
}


class LoginBackendProvider(object):

    def __init__(self, request):
        """Creates a login backup provider to be used by views.
        """
        self._request = request
        self._profile = None

        self.last_name = self._request.profile.last_login_backend_name
        if self.last_name:
            self.last = LOGIN_MODULES[self.last_name]['backend'](request)
        else:
            self.last = None
        self.current = self.last
        self.current_name = self.last_name

    def getCurrentProfile(self):
        if not self.current:
          return None

        if self._profile:
          return self._profile
        else:
          ProfileModel = LOGIN_MODULES[self.current_name]['profile']
          self._profile = ProfileModel.objects.filter(
              userprofile=self._request.profile)
          return self._profile

    def useBackend(self, name):
        """Use backend as current backend.
        """
        self.current = LOGIN_BACKEND_MODULES[name](self._request)
        self.current_name = name
        self._profile = None

    def getCurrentBackend(self):
        """Get current backend.
        """
        return self.current, self.current_name

    def getLastBackend(self):
        """Get last logged in backend.
        """
        return self.last, self.last_name


class LoginMiddleware(object):

    def process_request(self, request):
        self.request.profile = self.request.user.get_profile()

        self.request.login_backend = LoginBackendProvider(request)
        if not self.request.profile.is_initialized:
            #initialize profile
            #path_to_image = self.request.backend.getProfilePicture()
            pass
