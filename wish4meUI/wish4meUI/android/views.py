from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from wish4meUI.facebook.views import androidLogin
from warnings import catch_warnings

@csrf_exempt
def facebook_login(request):
  if request.POST:
    print "post request"
    facebookID = request.POST['id']
    print "id = " + facebookID
    facebookEmail = request.POST['email']
    print "email = " + facebookEmail
    facebookAccessToken = request.POST['accessToken']
    print "acces token : " + facebookAccessToken
    if "username" in request.POST:
        facebookUsername = request.POST['username']
        print "user name = " + facebookUsername
    

    try:
        if "username" in request.POST:
            androidLogin(request, facebookID, facebookEmail, facebookAccessToken, facebookUsername)
        else:
            androidLogin(request, facebookID, facebookEmail, facebookAccessToken)
        print "user name of request = "
        print request.user.username
    
    except:
        print "Unexpected error:", sys.exc_info()[0]
    return HttpResponse(request.user.username, content_type="text/plain")
  else:                             #for no post request

    print "facebook login hit"
    facebookAccessToken = "BAADonrXpx6cBAC1CGSnU7zYxe0BQNe9IIHaaK8B8VZBqYsMhx8h9xU7kVosMqYBZClWHn5oMgOJZA0pkQflZCWmd5VvmtownF0PzZBDQxunXZBMAZCI6ZBfpu4D0j7cyvdUZD"
    androidLogin(request, 15, "enginmanap@gmail.com", facebookAccessToken, "enginmanap")

  return HttpResponseRedirect(reverse('homePage'))

def newIdea(request):
    print "new idea is requested by "+ request.user.username
    response =  HttpResponse("nothing so far", content_type="text/plain")
    return response