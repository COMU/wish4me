#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wish4meUI.wish.models import WishCategory
from wish4meUI.wish.models import Wish


def welcome(request):
  if WishCategory.objects.all().count() < 1:
    wc = WishCategory(name="Default")
    wc.save()
 
  recent_wishes = Wish.objects.all().order_by('request_date')
  context = {"recent_wishes": recent_wishes}
  return render_to_response("home/welcome.html",
                            context_instance=RequestContext(request,
                                                            context))

def home(request):
  return render_to_response("home/home.html",
                            context_instance=RequestContext(request, {}))
