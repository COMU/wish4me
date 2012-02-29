import cgi, urllib, json, urllib2, oauth, httplib
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from twitter_app.utils import *

def home(request):
    print "home"
    return HttpResponseRedirect('/')

def facebook(request):
    username = request.GET.get('username', '')
    id = request.GET.get('id', '')
    message = request.GET.get('message', '')
    token = request.GET.get('access_token', '')
    name = 'follow {}'.format(username)
    link = 'http://wish4me.com/{}'.format(username)
    actions = ({
             'name' : name,
             'link' : link,
              })
    if id and message and token:
    	url = 'https://graph.facebook.com/id/feed'
    	values = {'message' : message,
        	     'access_token' : token,
        	     'actions' : actions,
        	 }
    	data = urllib.urlencode(values)
    	req = urllib2.Request(url, data)
    	response = urllib2.urlopen(req)
    return HttpResponseRedirect('/')

def twitter(request):
    CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    CONNECTION = httplib.HTTPSConnection(SERVER)
    message = request.GET.get('message', '')
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token)
    update_status(CONSUMER, CONNECTION, token, message)
    return HttpResponseRedirect('/')
