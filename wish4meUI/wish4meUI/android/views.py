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
from wish4meUI.friend.utils import getFollowingWishes

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
    response = "<login><username>"+request.user.username+"</username><session_id>"+request.session.session_key+"</session_id></login>"
    print response
    return HttpResponse(response, content_type="text/plain")
  else:                             #for no post request
    print "This url is for android app only."
  return HttpResponse("This url is for android app only.")

@csrf_exempt
@session_from_http_params
def listMyWishes(request):
    print "requested by : ",request.user.username
    wish_list = Wish.objects.filter(related_list__owner=request.user, is_hidden=False).order_by("-request_date")
    
    return render_to_response("android/wishlist.xml", {'wish_list': wish_list,})

@csrf_exempt
@session_from_http_params
def listFollowingWishes(request):
    print "requested by : ",request.user.username
    wish_list = getFollowingWishes(request)
    return render_to_response("android/wishlist.xml", {'wish_list': wish_list,})
