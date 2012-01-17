#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from wish4meUI.wish.forms import WishForm, WishCategoryForm
from wish4meUI.wish.models import Wish, WishCategory

def homeWish(request):
    context = dict()
    return render_to_response("wish/wish.html",
                              context_instance=RequestContext(request, context))

def addWish(request):
    if request.POST:
        form = WishForm(request.POST)
        if form.is_valid():
            pass

def listWish(request, wish_category_id=0):
    pass

def listWishCategory(request):
    context = dict()
    wish_category_list = WishCategory.objects.filter(is_approved=True)

    return render_to_response('wish/listWishCategory.html', {'wish_category_list':wish_category_list}, context_instance=RequestContext(request, context))
