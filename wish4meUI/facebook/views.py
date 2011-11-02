import cgi, urllib, json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

def facebook_auth(token=None, request=None):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
        'code': token,
    }
    target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
    response = cgi.parse_qs(target)
    access_token = response['access_token'][-1]

    fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
    fb_profile = json.load(fb_profile)

    return fb_profile

def authentication_callback(request):
    code = request.GET.get('code')
    user = facebook_auth(token=code, request=request)
    print "hede"
    auth_login(request, user)
    return HttpResponseRedirect('/')

def login(request):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))


def home(request):
    facebook_profile = ""
    print "hello"
    return render_to_response('facebook/home.html')
