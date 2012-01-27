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
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangoLogin
from django.template import RequestContext

from userprofile.models import *

CLIENT_ID = settings.FOURSQ_CLIENT_ID
CLIENT_SECRET = settings.FOURSQ_CLIENT_SECRET

request_token_url = 'https://foursquare.com/oauth2/authenticate'
access_token_url = 'https://foursquare.com/oauth2/access_token'
redirect_url = settings.BASE_URL + '/foursq/callback'

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
    return HttpResponseRedirect(reverse('foursq_oauth_done'))

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
    firstname = user['firstName']
    lastname = user['lastName']
    contact = user['contact']
    email = contact['email']
    foursq_id = user['id']
    userDetails = {'firstname':firstname, 'lastname':lastname, 'foursq_id':foursq_id, 'access_token':access_token, 'email' : email}
    return userDetails

def done(request):

    #write the authenticate method here
    credentials = foursquareUserDetails(request)
    user = authenticate(request=request, credentials=credentials, backend="foursq")

    if not user:
        return HttpResponse(reverse('user_loginFail'))

    response = HttpResponseRedirect(reverse('user_loginSuccess'))
    djangoLogin(request, user)
    return response

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
        #foursq_user = Foursq_User.objects.get(foursq_id=user_id)
        for friend_id in request.POST.getlist('friend_id'):
            foursq_friend = Foursq_Friend.objects.create(foursq_id=friend_id)
            # addind the index for many to many field
            #foursq_friend.foursq_user.add(foursq_user)
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


