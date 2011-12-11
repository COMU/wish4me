from django.contrib.auth.models import User
from userprofile.models import *
from django.http import *


def userLogin(request, loginFrom, loginID, userName):
    if loginFrom == 'twitter':
        access_token = request.session.get('access_token', None)
        try:
            userProfile = UserProfile.objects.get(TwitterID = loginID)
            
            if settings.DEBUG:
                print 'The user exists'
            userProfile.TwitterToken = access_token
            userProfile.save()
        except UserProfile.DoesNotExist:
            if settings.DEBUG:
                print 'The user not exists'
            newUser = User.objects.create_user(userName, settings.DEFAULT_EMAIL, settings.DEFAULT_PASSWORD)
            newUser.save()
            userProfile = UserProfile(user = newUser, TwitterID = loginID, TwitterToken = access_token)
            userProfile.save()  
