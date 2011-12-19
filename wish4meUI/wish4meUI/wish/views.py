#! -*- coding: utf-8 -*-
# Create your views here.

from django.forms import ModelForm
from django.shortcuts import render_to_response

from wish4meUI.wish.models import Wish


def home(request):
  return render_to_response("base.html", {})


class WishForm(ModelForm):
  class Meta:
    model = Wish


def add_wish(request):
  if request.POST:
    form = WishForm(request.POST)
    if form.is_valid():
      pass
