import urllib, urllib2, httplib, re
from django.shortcuts import render_to_response
from facebook.models import FacebookProfile


def facebook_contact_import(request):

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
    x = re.findall(r'"\d+"',response)
    friend_list = [a.strip('"') for a in x]
    #friends_count = len(friend_list) #not really needed, but may come in handy
    return friend_list

