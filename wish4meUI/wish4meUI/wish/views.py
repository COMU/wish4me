#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_list_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishlistForm
from wish4meUI.wish.models import Wish, WishCategory, Wishlist

def homeWish(request):
    wishlists = Wishlist.objects.filter(owner=request.user)
    wishlistForm = WishlistForm()

    return render_to_response('wish/wish.html', {'wishlists':wishlists, 'WishlistForm': wishlistForm}, context_instance=RequestContext(request))

def addWish(request):
    if request.POST:
        form = WishForm(request.POST)
        if form.is_valid():
            pass

def addWishlist(request):
  if request.POST:
    form = WishlistForm(request.POST)
    if form.is_valid():
      wishlist = form.save(commit = False)
      wishlist.owner = request.user
      wishlist.comment = form.cleaned_data['comment']
      wishlist.save()
      return HttpResponseRedirect(reverse('home'))
  else:
    pass


def listWishlist(request):
    wishlists = Wishlist.objects.filter(owner=request.user)

    return render_to_response('wish/listWishlist.html', {'wishlists':wishlists}, context_instance=RequestContext(request))

def listWish(request, wish_category_id=0):
    pass

def listWish(request, wishlist_id=0):
    context = dict()
    wish_list = Wish.objects.filter(related_list__id=wishlist_id)

    return render_to_response('wish/listWish.html', {'wish_list':wish_list}, context_instance=RequestContext(request, context))

def listWishCategory(request):
    context = dict()
    wish_category_list = WishCategory.objects.filter(is_approved=True)

    return render_to_response('wish/listWishCategory.html', {'wish_category_list':wish_category_list}, context_instance=RequestContext(request, context))
