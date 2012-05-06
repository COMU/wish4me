import cgi, urllib, json, datetime, urllib2

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse

from facebook.forms import NewsFeedForm
from facebook.models import FacebookNewsFeed
from facebook.models import FacebookProfile


def login(request):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri(reverse(
            'facebook_login_callback')),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def androidLogin(request, facebookID, facebookEmail, access_token, facebookUsername=None):
    print "android logon try"
    user = authenticate(request=request, id=facebookID, email=facebookEmail, username=facebookUsername, access_token = access_token)
    print "android logged in"
    if user.is_authenticated():
      auth_login(request, user)
    return request.user

def loginCallback(request):
    code = request.GET.get('code')
    user = authenticate(request=request, token=code)
    if user.is_authenticated():
      auth_login(request, user)
    return HttpResponseRedirect(reverse('user_loginSuccess'))


def home(request):
    try:
      facebook_profile = request.user.get_profile().get_facebook_profile()
    except:
      facebook_profile = ""
    return render_to_response('facebook/home.html',
    	                          { 'facebook_profile': facebook_profile, 'newsfeed_form': NewsFeedForm() },
    	                          context_instance=RequestContext(request))


def newsfeed(request):

  facebook_profile = request.user.get_profile().get_facebook_profile()
  message = request.POST.get('message', '')
  facebook_pub = request.POST.get('facebook_pub', '')
  token = FacebookProfile.objects.get(facebook_id=facebook_profile['id'])
  token = token.access_token

  if message and facebook_pub and facebook_profile:

	fb_newsfeed = FacebookNewsFeed(message=message, facebook_id=facebook_profile['id'], 
                                  date=datetime.datetime.now(), facebook_pub=facebook_pub)
  fb_newsfeed.save()
  if facebook_pub == '1':
    url = 'https://graph.facebook.com/me/feed'
    values = {'message' : message,
              'access_token' : token }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)

    return render_to_response('facebook/home.html',
                              { 'facebook_profile': facebook_profile, 'newsfeed_form': NewsFeedForm() },
                                context_instance=RequestContext(request))

