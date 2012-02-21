#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wish4meUI.wish.models import WishCategory

def welcome(request):
  if WishCategory.objects.all().count() < 1:
    wc = WishCategory(name="Default")
    wc.save()
 
  return render_to_response("home/welcome.html",
                            context_instance=RequestContext(request, {}))
