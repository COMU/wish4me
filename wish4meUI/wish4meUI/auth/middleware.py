#!/usr/bin/python
# -*- coding: utf-8 -*-

from wish4meUI.settings import LOGIN_BACKEND_MODULES


class LoginBackendProvider(object):

    def __init__(self, request):
        """Creates a login backup provider to be used by views.
        """
        self.last_name = request.session.get('last_login_backend_name')
        if self.last_name:
            self.last = LOGIN_BACKEND_MODULES.get(self.last_name)(request)
        else:
            self.last = None
        self.current = self.last
        self.current_name = self.last_name

        self._request = request

    def useBackend(self, name):
        """Use backend as current backend.
        """
        self.current = LOGIN_BACKEND_MODULES[name](self._request)
        self.current_name = name

    def getCurrent(self):
        """Get current backend.
        """
        return self.current, self.current_name

    def getLast(self):
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
