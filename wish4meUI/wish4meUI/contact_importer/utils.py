import json, oauth, urllib, urllib2, httplib, re
from django.shortcuts import render_to_response
from facebook.models import FacebookProfile
from twitter_app.utils import *
from foursq.models import FoursqProfile
try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise "Requires either simplejson, Python 2.6 or django.utils!"

def facebook_contact_import(request):
    friends_list=[]
    user = request.user
    profile = user.get_profile()
    fb_id = profile.facebook_profile_id
    token = FacebookProfile.objects.get(id=fb_id)
    token = token.access_token
    values = {}
    values['access_token'] = token
    url_values = urllib.urlencode(values)
    url = 'https://graph.facebook.com/me/friends'
    full_url = url + '?' + url_values
    response = urllib2.urlopen(full_url)
    response = response.read()
    json = simplejson.loads(response)
    for i in json.get('data','0'):
      i=i.get('id','0')
      friends_list.append(i)
    return friends_list


def twitter_contact_import(request):
    friends_list = []
    CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    CONNECTION = httplib.HTTPSConnection(SERVER)
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token)
    auth = is_authenticated(CONSUMER, CONNECTION, token)
    if auth:
        creds = simplejson.loads(auth)
        name = creds.get('name', creds['screen_name']) # Get the name

        # Get number of friends. The API only returns 100 results per page,
        # so we might need to divide the queries up.
        friends_count = str(creds.get('friends_count', '100'))
        pages = int( (int(friends_count)/100) ) + 1
        pages = min(pages, 10) # We only want to make ten queries
        for page in range(pages):
          friends = get_friends(CONSUMER, CONNECTION, token, page+1)
          if friends == '[]': break
    json = simplejson.loads(friends)
    for i in json.get('ids','0'):
      print i
      friends_list.append(i)
    return friends_list
    
def google_contact_import(request):
    print request.session.get('access_token')
    
    
def foursquare_contact_import(request):
    friends_list=[]
    user = request.user
    profile = user.get_profile()
    foursq_id = profile.foursq_profile_id
    token = FoursqProfile.objects.get(id=foursq_id)
    token = token.access_token
    values = {}
    values['oauth_token'] = token
    url_values = urllib.urlencode(values)
    url = 'https://api.foursquare.com/v2/users/self/friends'
    full_url = url + '?' + url_values
    friends = urllib2.urlopen(full_url)
    friends = friends.read()
    json = simplejson.loads(friends)
    json=json.get('response','0')
    json=json.get('friends','0')
    json=json.get('items','0')
    for i in json:
      i=i.get('id','0')
      friends_list.append(i)
    return friends_list
    
