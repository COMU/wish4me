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

CLIENT_ID = '1OVOPIR5HS5XEXJYNB4B1QNCPLFLIVULYCGHT3BFSNCG5HMR'
CLIENT_SECRET = 'JKYYZB5FIDQEHIE3MB4VZARVWWTEZTN1ICOAK1IPFBCHSSQH'

request_token_url = 'https://foursquare.com/oauth2/authenticate'
access_token_url = 'https://foursquare.com/oauth2/access_token'
redirect_url = settings.BASE_URL + '/foursq_auth/callback'

def main(request):
    return render_to_response('foursq_auth/login.html')

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
    return HttpResponseRedirect(reverse('main'))

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
    name = " ".join([user['firstName'], user['']])
    contact = user['contact']
    email = contact['email']
    obj, created = User.objects.get_or_create(email, email)
    if not created:
        # create the user with the username and email as his/her email
        passwd = User.objects.make_random_password()
        obj.set_password(passwd)
        obj.save()
    user_obj = User.objects.get(email=email)
    user = authenticate(username=email, password=user_obj.password)
    if user is not None:
        if user.is_active:
              login(request, user)
              # show the page with the user's name to show they've logged in
              return render_to_response('foursq_auth/done.html', {'name':name})
        else:
            return render_to_response('errors/disabled_account.html', {'name', name})
    else:
        return render_to_response('errors/invalid_login', {'name', name})

