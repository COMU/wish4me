#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def welcome(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse("listAllWishes"))
  else:
    return render_to_response("home/welcome.html",
                            context_instance=RequestContext(request, {}))
