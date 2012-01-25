import oauth, httplib, time, datetime

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

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from twitter_app.utils import *
from userprofile.models import *
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as djangoLogin
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(SERVER)
print "SERVER:", SERVER, "CONNECTION:", CONNECTION


def main(request):
    if request.session.has_key('access_token'):
        return HttpResponseRedirect(reverse('twitter_oauth_user_details'))
    else:
        return render_to_response('twitter_app/base.html')

def unauth(request):
    response = HttpResponseRedirect("/home")
    del request.session['access_token']
    del request.session['unauthed_token']
    close_twitter_connection(CONNECTION)
    logout(request)
    #request.session.clear()
    return response

def auth(request):
    "/auth/"
    connect_twitter(CONNECTION)
    token = get_unauthorised_request_token(CONSUMER, CONNECTION)
    auth_url = get_authorisation_url(CONSUMER, token)
    response = HttpResponseRedirect(auth_url)
    request.session['unauthed_token'] = token.to_string()
    return response

def return_(request):
    "/return/"
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie.")
    token = oauth.OAuthToken.from_string(unauthed_token)
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    verifier = request.GET.get('oauth_verifier')
    access_token = exchange_request_token_for_access_token(CONSUMER, token, params={'oauth_verifier':verifier})
    response = HttpResponseRedirect(reverse('user_loginSuccess'))
    request.session['access_token'] = access_token.to_string()

    #it seems, authorization request does not return any data about user.
    #we request data via verify_credentials because it is easiest.
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token)
    auth = is_authenticated(CONSUMER, CONNECTION, token)

    if auth:
        creds = simplejson.loads(auth)
        user = authenticate(request=request, credentials=creds)
        if not user:
          print "user was not authenticated"
          return HttpResponseRedirect(reverse('user_loginFail'))
        djangoLogin(request, user)
    return response


def twitterUserDetails(request):
    access_token = request.session.get('access_token', None)
    token = oauth.OAuthToken.from_string(access_token)
    #is_authenticated returns user details as well
    auth = is_authenticated(CONSUMER, CONNECTION, token)

    if auth:
        creds = simplejson.loads(auth)
        userName = creds.get('screenName', creds['screen_name'])

    userDetails = { 'userName' : userName,}
    return userDetails

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

def userDetails(request):
    access_token = request.session.get('access_token', None)
    if not access_token:
        return HttpResponse("You need an access token!")
    token = oauth.OAuthToken.from_string(access_token)

    # Check if the token works on Twitter
    auth = is_authenticated(CONSUMER, CONNECTION, token)
    if auth:
        # Load the credidentials from Twitter into JSON
        creds = simplejson.loads(auth)
        screenName = creds.get('name', creds['screen_name']) # Get the name
        name = creds.get('name', creds['name']) # Get the name
    userID = creds.get('ID', creds['id']) # Get the user ID
    userDetails = { 'screenName' : screenName, 'name' : name, 'ID' : userID }
    if request.user.is_authenticated:
	    print "yes"
    else:
      print "no"
    return render_to_response('twitter_app/user.html', {'userDetails': userDetails}, context_instance=RequestContext(request))

def friend_list(request):
    users = []

    access_token = request.session.get('access_token', None)
    if not access_token:
        return HttpResponse("You need an access token!")
    token = oauth.OAuthToken.from_string(access_token)

    # Check if the token works on Twitter
    auth = is_authenticated(CONSUMER, CONNECTION, token)
    if auth:
        # Load the credidentials from Twitter into JSON
        creds = simplejson.loads(auth)
        name = creds.get('name', creds['screen_name']) # Get the name

        # Get number of friends. The API only returns 100 results per page,
        # so we might need to divide the queries up.
        friends_count = str(creds.get('friends_count', '100'))
        pages = int( (int(friends_count)/100) ) + 1
        pages = min(pages, 10) # We only want to make ten queries



        for page in range(pages):
            friends = get_friends(CONSUMER, CONNECTION, token, page+1)

            # if the result is '[]', we've reached the end of the users friends
            if friends == '[]': break
        #get details for given list of friend IDs
        friendDetails = get_friend_details(CONSUMER, CONNECTION, token, friends)
        # Load into JSON
        json = simplejson.loads(friendDetails)
        users.append(json)
    return render_to_response('twitter_app/list.html', {'users': users})
