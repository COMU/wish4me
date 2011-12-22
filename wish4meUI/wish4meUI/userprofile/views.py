from userprofile.models import *
from django.contrib.auth.models import User
from django.http import *
from twitter_app.views import *
from django.contrib.auth import authenticate, login

def getUserDetails(request, loginFrom):
    from twitter_app.views import twitterUserDetails
    if loginFrom == 'twitter':
        details = twitterUserDetails(request)
    return details

def userLogin(request, loginFrom, loginID):
    if loginFrom == 'twitter':
        access_token = request.session.get('access_token', None)
        try:
            userProfile = UserProfile.objects.get(TwitterID = loginID)
            if settings.DEBUG:
                print 'The user exists'
            userProfile.TwitterToken = access_token
        except UserProfile.DoesNotExist:
            if settings.DEBUG:
                print 'The user not exists'
            userDetails = getUserDetails(request, loginFrom)
            #userDetails = twitterUserDetails(request)
	    print "userDetails are:", userDetails
            newUser = User.objects.create_user(userDetails['userName'], settings.DEFAULT_EMAIL, settings.DEFAULT_PASSWORD)
            newUser.save()
            userProfile = UserProfile(user = newUser, TwitterID = loginID, TwitterToken = access_token)
        userName = userProfile.user.username
        userProfile.save()  
	
	#login part
	user = authenticate(username=userName, password=settings.DEFAULT_PASSWORD)
	if user is not None:
	    if user.is_active:
		login(request, user)
	    else:
		print "Your account has been disabled!"
	else:
	    print "Your username and password were incorrect."	


	return userProfile
