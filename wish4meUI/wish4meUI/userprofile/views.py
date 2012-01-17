from userprofile.models import *
from django.contrib.auth.models import User
from django.http import *
from twitter_app.views import *
from django.contrib.auth import authenticate, login

def getUserDetails(request, loginFrom):
    from twitter_app.views import twitterUserDetails	#imports must be here or wont work
    from foursq.views import foursquareUserDetails
    if loginFrom == 'twitter':
        details = twitterUserDetails(request)
    elif loginFrom == 'foursquare':
	details = foursquareUserDetails(request)
    return details

def userLogin(request, loginFrom, loginID):

    try:
	#add the search parameter here:
        if loginFrom == 'twitter':
            userProfile = UserProfile.objects.get(TwitterID = loginID)
        elif loginFrom == 'foursquare':
            userProfile = UserProfile.objects.get(FoursquareID = loginID)
	else:
	    print "the login attemp does not provide a valid \"loginFrom\" "
            return none
	#end of search parameters
        if settings.DEBUG:
	    print 'The user exists'

	# add what to do if user exists here:
        if loginFrom == 'twitter':
            access_token = request.session.get('access_token', None)
            userProfile.TwitterToken = access_token
	elif loginFrom == 'foursquare':
            access_token = request.session.get('access_token', None)
            userProfile.FoursqareToken = access_token
	#end of user exists part
	userProfile.save()
    except UserProfile.DoesNotExist:
        if settings.DEBUG:
	    print 'The user not exists'
        userDetails = getUserDetails(request, loginFrom)
        newUser = User.objects.create_user(userDetails['userName'], settings.DEFAULT_EMAIL, settings.DEFAULT_PASSWORD)
        newUser.save()
        access_token = request.session.get('access_token', None)

	
	# add what to do if user is not exists here:
        if loginFrom == 'twitter':	
        	userProfile = UserProfile(user = newUser, TwitterID = loginID, TwitterToken = access_token)
        if loginFrom == 'foursquare':	
        	userProfile = UserProfile(user = newUser, FoursquareID = loginID, FoursquareToken = access_token)
	#end of user exists part
        userProfile.save()  
	
    #login part
    userName = userProfile.user.username
    user = authenticate(username=userName, password=settings.DEFAULT_PASSWORD)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            print "Your account has been disabled!"
    else:
        print "Your username and password were incorrect."	

    return userProfile
