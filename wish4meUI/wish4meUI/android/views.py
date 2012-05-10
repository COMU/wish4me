from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from warnings import catch_warnings
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from wish4meUI.facebook.views import androidLogin
from wish4meUI.decorators.cookieless_decorator  import session_from_http_params
from wish4meUI import settings
from wish4meUI.wish.models import Wish

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

    return HttpResponse(request.session.session_key, content_type="text/plain")
  else:                             #for no post request

    print "facebook login hit"
    facebookAccessToken = "BAADonrXpx6cBAC1CGSnU7zYxe0BQNe9IIHaaK8B8VZBqYsMhx8h9xU7kVosMqYBZClWHn5oMgOJZA0pkQflZCWmd5VvmtownF0PzZBDQxunXZBMAZCI6ZBfpu4D0j7cyvdUZD"
    androidLogin(request, 15, "enginmanap@gmail.com", facebookAccessToken, "enginmanap")

  return HttpResponseRedirect(reverse('homePage'))

@csrf_exempt
@session_from_http_params
def listMyWishes(request):
    print "requested by : ",request.user.username
    wish_list = Wish.objects.filter(related_list__owner=request.user, is_hidden=False).order_by("-request_date")
    
    return render_to_response("android/wishlist.xml", {'wish_list': wish_list,})

@csrf_exempt
@session_from_http_params
def newIdea(request):
    response =  HttpResponse("nothing so far", content_type="text/plain")
    return response