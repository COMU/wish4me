#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wish4meUI.wish.models import WishCategory
from wish4meUI.friend.models import Following
from wish4meUI.wish.models import Wish

from django.db import connection


def list_friends_wishes(request):
  following_list = Following.objects.filter(from_user = request.user).values('to_user_id')
  #print(str(Wish.objects.filter(related_list__owner__in = following_list).query))
  wishes = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False).order_by("-request_date")[:5]
  return render_to_response("home/list_friend_wishes.html", {'wish_list' : wishes, }, context_instance=RequestContext(request, {}))

def welcome(request):
  if WishCategory.objects.all().count < 1:
    wc = WishCategory(name="Default")
    wc.save()
 
  return render_to_response("home/welcome.html",
                            context_instance=RequestContext(request, {}))
