#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import urllib
import urllib2
import json

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from foursq.models import Foursq_User, Foursq_Friend
from userprofile.models import *
from userprofile.views import *

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

def foursquareUserDetails(request):
    # get the access_token
    access_token = request.session.get('access_token')

    # request user details from foursquare
    params = { 'oauth_token' : access_token }
    data = urllib.urlencode(params)
    url = 'https://api.foursquare.com/v2/users/self'
    full_url = url + '?' + data
    response = urllib2.urlopen(full_url)
    response = response.read()
    user = json.loads(response)['response']['user']
    name = "".join([user['firstName'], user['lastName']])
    contact = user['contact']
    email = contact['email']
    id = user['id']
    userDetails = {'userName' : name, 'email' : email,}
    return userDetails

def done(request):
    # get the access_token
    access_token = request.session.get('access_token')

    # request user details from foursquare
    params = { 'oauth_token' : access_token }
    data = urllib.urlencode(params)
    url = 'https://api.foursquare.com/v2/users/self'
    full_url = url + '?' + data
    response = urllib2.urlopen(full_url)
    response = response.read()
    user = json.loads(response)['response']['user']
    name = "".join([user['firstName'], user['lastName']])
    contact = user['contact']
    email = contact['email']
    id = user['id']
    request.session['user_id'] = id
    print "id", id
    auth_user = userLogin(request, "foursquare", id)
    #authenticated user object
    if auth_user is not None:
        if auth_user.user.is_active:
              # show the page with the user's name to show they've logged in
              return render_to_response('foursq/done.html', {'name':name})
        else:
            return render_to_response('errors/disabled_account.html', {'name', name})
    else:
        return render_to_response('errors/invalid_login.html', {'name', name})

def friend_import(request):
    send_data = {}
    send_data.update(csrf(request))
    # get the access_token
    access_token = request.session.get('access_token')

    # request user details from foursquare
    params = { 'oauth_token' : access_token }
    data = urllib.urlencode(params)

    if request.method == 'POST':
        user_id = request.session['user_id']
        foursq_user = Foursq_User.objects.get(foursq_id=user_id)
        for friend_id in request.POST.getlist('friend_id'):
            foursq_friend = Foursq_Friend.objects.create(foursq_id=friend_id)
            # addind the index for many to many field
            foursq_friend.foursq_user.add(foursq_user)
            send_data.update({'message':'ok'})
            return render_to_response('foursq/success.html', send_data)

    else:
        url = 'https://api.foursquare.com/v2/users/self/friends'
        full_url = url + '?' + data
        response = urllib2.urlopen(full_url)
        response = response.read()
        friends = json.loads(response)['response']['friends']
        items = friends['items']
        send_data.update({'items':items})
        return render_to_response('foursq/friend_import.html', send_data)


