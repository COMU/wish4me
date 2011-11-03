#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import urllib2
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from foursq.models import Foursq_User

CLIENT_ID = settings.FOURSQ_CLIENT_ID
CLIENT_SECRET = settings.FOURSQ_CLIENT_SECRET

request_token_url = 'https://foursquare.com/oauth2/authenticate'
access_token_url = 'https://foursquare.com/oauth2/access_token'
redirect_url = settings.BASE_URL + '/foursq_auth/callback'

def main(request):
    return render_to_response('foursq/login.html')

def auth(request):
    # build the url to request
    params = {'client_id' : CLIENT_ID,
            'response_type' : 'code',
            'redirect_uri' : redirect_url}
    data = urllib.urlencode(params)
    # redirect the user to the url to confirm access for the app
    return HttpResponseRedirect('%s?%s' % (request_token_url, data))

def unauth(request):
    # clear any tokens and logout
    request.session.clear()
    logout(request)
    return HttpResponseRedirect(reverse('main_view'))

def callback(request):
   # get the code returned from foursquare
    code = request.GET.get('code')

    # build the url to request the access_token
    params = { 'client_id' : CLIENT_ID,
               'client_secret' : CLIENT_SECRET,
               'grant_type' : 'authorization_code',
               'redirect_uri' : redirect_url,
               'code' : code}
    data = urllib.urlencode(params)
    req = urllib2.Request(access_token_url, data)

    # request the access_token
    response = urllib2.urlopen(req)
    access_token = json.loads(response.read())
    access_token = access_token['access_token']

    # store the access_token for later use
    request.session['access_token'] = access_token

    # redirect the user to show we're done
    return HttpResponseRedirect(reverse('oauth_done'))

def done( request ):
    # get the access_token
    access_token = request.session.get('access_token')

    # request user details from foursquare
    params = { 'oauth_token' : access_token }
    data = urllib.urlencode(params)
    url = 'https://api.foursquare.com/v2/users/self'
    full_url = url + '?' + data
    print full_url
    response = urllib2.urlopen(full_url)
    response = response.read()
    user = json.loads(response)['response']['user']
    name = " ".join([user['firstName'], user['lastName']])
    contact = user['contact']
    email = contact['email']
    id = user['id']
    print "id", id

    #check whether this user has logged before, if not create a default User object for it
    foursq_user = Foursq_User.objects.filter(foursq_id=id)
    if not foursq_user:
        user = User.objects.create(username=email, email=email)
        Foursq_User.objects.create(foursq_id=id, user=user)
        #create a default password for the system users, no need to reflect it to the user, the user can change it anytime from the dashboard
        password = User.objects.make_random_password()
        print "password", password
        user.set_password(password)
        user.save()
    else:
        user = foursq_user[0].user

    print "authenticating", user.email, user.password
    #authenticated user object
    auth_user = authenticate(username=user.email, password=user.password)
    if auth_user is not None:
        if auth_user.is_active:
              login(request, auth_user)
              # show the page with the user's name to show they've logged in
              return render_to_response('foursq/done.html', {'name':name})
        else:
            return render_to_response('errors/disabled_account.html', {'name', name})
    else:
        return render_to_response('errors/invalid_login.html', {'name', name})

