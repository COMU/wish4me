from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from warnings import catch_warnings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User

from wish4meUI.facebook.views import androidLogin
from wish4meUI.decorators.cookieless_decorator  import session_from_http_params
from wish4meUI import settings
from wish4meUI.wish.models import Wish, WishCategory
from wish4meUI.wishlist.models import Wishlist
from wish4meUI.friend.utils import getFollowingWishes
from datetime import datetime
import sys

@csrf_exempt
def facebook_login(request):
  if request.POST:
    facebookID = request.POST['id']
    facebookEmail = request.POST['email']
    facebookAccessToken = request.POST['accessToken']
    if "username" in request.POST:
        facebookUsername = request.POST['username']
        print "user name = " + facebookUsername
    try:
        if "username" in request.POST:
            androidLogin(request, facebookID, facebookEmail, facebookAccessToken, facebookUsername)
        else:
            androidLogin(request, facebookID, facebookEmail, facebookAccessToken)
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

@csrf_exempt
@session_from_http_params
def add_new_wish(request):
  print "session key is ", request.session.session_key
  if request.POST:
      try:
        wish_brand = request.POST['brand']
        print "1 : ",wish_brand
        wish_name = request.POST['name']
        print "2 : ",wish_name
        wish_description = request.POST['description']
        print "3 : ",wish_description
        #request.user = User.objects.get(pk=2)
        print "4 : ",request.user.username
        wish = Wish(wish_for = request.user, 
                    description = wish_description, 
                    name=wish_name, 
                    brand=wish_brand, 
                    category=WishCategory.objects.get(pk=1), 
                    related_list=Wishlist.objects.filter(owner=request.user, is_hidden=False)[0], 
                    request_date = datetime.now())
        wish.save()
        if request.FILES:
            if request.FILES['wishphoto_0']:
                print "there is a file"

        response = "<wish><result>success</result><session_id>"+request.session.session_key+"</session_id></wish>"
        print response
        return HttpResponse(response, content_type="text/plain")
      except:
        print "Unexpected error:", sys.exc_info()[0]
  return HttpResponse("<wish><result>fail</result><session_id>"+request.session.session_key+"</session_id></wish>", content_type="text/plain")
