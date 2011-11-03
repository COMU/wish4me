import cgi, urllib, json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

def authentication_callback(request):
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)
    print user
    auth_login(request, user)
    return HttpResponseRedirect('/facebook/')

def login(request):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))


def home(request):
    try:
        facebook_profile = request.user.get_profile().get_facebook_profile()
    except:
        facebook_profile = ""
    return render_to_response('facebook/home.html',
                              { 'facebook_profile': facebook_profile },
                              context_instance=RequestContext(request))
