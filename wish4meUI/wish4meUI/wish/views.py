#! -*- coding: utf-8 -*-
# Create your views here.

from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from wish4meUI.wish.models import Wish


def home(request):
    context = dict()
    return render_to_response("home/home.html",
                              context_instance=RequestContext(request, context))

class WishForm(ModelForm):
    class Meta:
        model = Wish

def add_wish(request):
    if request.POST:
        form = WishForm(request.POST)
        if form.is_valid():
            pass
