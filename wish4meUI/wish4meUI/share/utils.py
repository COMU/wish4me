import cgi, urllib, json, urllib2, oauth, httplib
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from twitter_app.utils import *
from facebook.models import FacebookProfile
from wish4meUI.wish.models import Wish

def facebook_share(request, id):
    thing = 'http://127.0.0.1:8000/share/show/{}'.format(id)
    user = request.user
    profile = user.get_profile()
    fb_id = profile.facebook_profile_id
    token = FacebookProfile.objects.get(id=fb_id)
    token = token.access_token
    url = 'https://graph.facebook.com/me/neistediginibilirsin:wish'
    values = {   'access_token' : token,
                 'thing' : thing,
             }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return HttpResponseRedirect('/')

def twitter_share(request, id):
    CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    CONNECTION = httplib.HTTPSConnection(SERVER)
    wish = get_object_or_404(Wish, pk=id)
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token) 
    message = Wish.objects.get(pk=id)
    message = message.description
    update_status(CONSUMER, CONNECTION, token, message)
    return HttpResponseRedirect('/')

