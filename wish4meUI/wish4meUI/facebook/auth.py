import cgi, urllib, json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse

from facebook.models import FacebookProfile

class FacebookBackend:

    def authenticate(self, request, **kwargs):
        """ if used with a token parameter, Reads in a Facebook code and asks Facebook if it's valid and what user it points to.
            if used with id and email,(optional username) creates the proper database entities."""
        if "token" in kwargs:

            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'redirect_uri': request.build_absolute_uri(
                    reverse('facebook_login_callback')),
                'code': kwargs['token'],
            }

            # Get a legit access token
            target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
            response = cgi.parse_qs(target)
            access_token = response['access_token'][-1]

            # Read the user's profile information
            fb_profile = urllib.urlopen(
              'https://graph.facebook.com/me?access_token=%s' % access_token)
            fb_profile = json.load(fb_profile)
        else:
            fb_profile = None
            if "id" in kwargs and "email" in kwargs:
                print "android authenticate func"
                if "username" in kwargs:
                    fb_profile = {'id' : kwargs['id'], 'email' : kwargs['email'], 'username' : kwargs['username']}
                else:
                    fb_profile = {'id' : kwargs['id'], 'email' : kwargs['email'], 'username' : kwargs['username']}

            if "access_token" in kwargs:
                access_token = kwargs['access_token']

        try:
          # Try and find existing user
          facebook_profile = FacebookProfile.objects.get(
              facebook_id=fb_profile['id'])

          # Update access_token
          facebook_profile.access_token = access_token
          facebook_profile.save()

        except FacebookProfile.DoesNotExist:
          # No existing user, create one
          facebook_profile = FacebookProfile(facebook_id=fb_profile['id'],
                                             access_token=access_token)
          facebook_profile.save()
        except Exception:
          return None
        backend = facebook_profile.getLoginBackend(request)
        try:
          fb_username=fb_profile['username']
        except:
          fb_username=fb_profile['email']

        try:
          fb_mail = fb_profile['email']
          user = backend.login(
            facebook_profile, related_name='facebook_profile',
            username=fb_username, email=fb_profile['email'])
        except:
          import sys
          print "error ", sys.exc_info()[0]
        return user

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    supports_object_permissions = False
    supports_anonymous_user = False
