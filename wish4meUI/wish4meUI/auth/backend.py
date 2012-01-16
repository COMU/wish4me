#!/usr/bin/python
# -*- coding: utf-8 -*-


class LoginBackend(object):
    """Provides a base class for all authentication
    backends for generic methods.
    """

    def __init__(self, request):
        self._request = request

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
