import cgi, urllib, json, urllib2
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def home(request):
    print "home"
    return HttpResponseRedirect('/')

def facebook(request):
username = request.GET.get('username', '')
fb_id = request.GET.get('fb_id', '')
fb_message = request.GET.get('fb_message', '')
fb_token = request.GET.get('fb_access_token', '')
fb_name = 'follow {}'.format(username)
fb_link = 'http://wish4me.com/{}'.format(username)
         actions = ({
             'name' : fb_name,
             'link' : fb_link,
         })
if fb_id and fb_message and fb_token:
url = 'https://graph.facebook.com/me/feed'
values = {'message' : fb_message,
         'access_token' : fb_token,
'actions' : actions,
          }
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
     print "success"
return HttpResponseRedirect('/')

def twitter(request):
    print "twitter"
    return HttpResponseRedirect('/')
