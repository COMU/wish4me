import oauth, urllib, urllib2, httplib, re
from django.shortcuts import render_to_response
from facebook.models import FacebookProfile
from twitter_app.utils import *
from foursq.models import FoursqProfile
try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise "Requires either simplejson, Python 2.6 or django.utils!"

def facebook_contact_import(request):

    user = request.user
    profile = user.get_profile()
    fb_id = profile.facebook_profile_id
    token = FacebookProfile.objects.get(id=fb_id)
    token = token.access_token
    values = {}
    values['access_token'] = token
    url_values = urllib.urlencode(values)
    url = 'https://graph.facebook.com/me/friends'
    full_url = url + '?' + url_values
    response = urllib2.urlopen(full_url)
    response = response.read()
    return response

def twitter_contact_import(request):
    CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    CONNECTION = httplib.HTTPSConnection(SERVER)
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token)
    friend_list = get_friends(CONSUMER, CONNECTION, token, page=0)
    return friend_list
    
def google_contact_import(request):
    print request.session.get('access_token')
    
    
def foursquare_contact_import(request):
    user = request.user
    profile = user.get_profile()
    foursq_id = profile.foursq_profile_id
    token = FoursqProfile.objects.get(id=foursq_id)
    token = token.access_token
    values = {}
    values['oauth_token'] = token
    url_values = urllib.urlencode(values)
    url = 'https://api.foursquare.com/v2/users/self/friends'
    full_url = url + '?' + url_values
    response = urllib2.urlopen(full_url)
    response = response.read()
    return response
    
