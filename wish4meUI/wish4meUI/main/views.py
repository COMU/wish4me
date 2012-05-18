#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from wish4meUI.wish.models import WishCategory, Wish
from wish4meUI.friend.models import Following

from django.db import connection
from django.conf import settings

import datetime

def list_friends_wishes(request):
  following_list = Following.objects.filter(from_user = request.user).values('to_user_id')
  friends_list = Following.objects.filter(from_user__in = following_list, to_user = request.user).values('from_user_id')

  #print(str(Wish.objects.filter(related_list__owner__in = following_list).query))
  wishes_from_friends = Wish.objects.filter(related_list__owner__in = friends_list, is_hidden = False)
  wishes_from_following = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False, is_private = False)
  wishes = wishes_from_friends | wishes_from_following
  wishes = wishes.order_by("-request_date")[:5]
  #wishes = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False).order_by("-request_date")[:5]
  return render_to_response("home/list_friend_wishes.html", {'wish_list' : wishes, }, context_instance=RequestContext(request, {}))

def welcome(request):
  if 'redirect' in request.GET:
    messages.add_message(request, messages.WARNING, "You need to login first!"),
  if WishCategory.objects.all().count() < 1:
    wc = WishCategory(name="Default")
    wc.save()

  context = {
      'page_title': 'Welcome to %s' % settings.PROJECT_NAME
  }
  if not request.user.is_authenticated():
    recent_wishes = Wish.objects.filter(is_private=False, is_hidden=False).order_by('request_date')
    context.update({"recent_wishes": recent_wishes})
    return render_to_response("home/welcome.html",
                            context_instance=RequestContext(request, context))
  else:
		if datetime.datetime.now() - request.user.date_joined < datetime.timedelta(minutes=1):
			return HttpResponseRedirect(reverse('helpPage'))
		return HttpResponseRedirect(reverse('friend-activity'))

def help(request):
	context = {
		'page_title': 'Help Page'
	}

	return render_to_response("home/help.html",
                            context_instance=RequestContext(request, context))

