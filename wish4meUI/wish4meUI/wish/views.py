#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_list_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from datetime import datetime

from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishlistForm
from wish4meUI.wish.models import Wish, WishCategory, Wishlist

def homeWish(request):
  wishlists = Wishlist.objects.filter(owner=request.user)
  wishlist_form = WishlistForm()

  return render_to_response('wish/wish.html', {'wishlists':wishlists, 'wishlist_form': wishlist_form}, context_instance=RequestContext(request))

def addWish(request, wishlist_id):
  if request.POST:
    form = WishForm(request.POST)
    if form.is_valid():
      wish = form.save(commit = False)
      wish.wish_for = request.user
      wish.description = form.cleaned_data['description']
      wish.name = form.cleaned_data['name']
      wish.brand = form.cleaned_data['brand']
      wish.category = form.cleaned_data['category']
      wish.request_date = datetime.now()
      wish.related_list = Wishlist.objects.get(pk=wishlist_id)
      wish.save()
      return HttpResponseRedirect(reverse('wish_list_wish', args=[wishlist_id]))
  else:
    wish_form = WishForm()
    return render_to_response('wish/add_wish.html', {'wish_form': wish_form, 'wishlist_id': wishlist_id}, context_instance=RequestContext(request))

def listAllWishes(request):
  wish_list = Wish.objects.filter(related_list__owner=request.user)

  return render_to_response('wish/list_wish.html', {'wish_list': wish_list, 'wishlist_id': 1}, context_instance=RequestContext(request))

def addWishlist(request):
  if request.POST:
    form = WishlistForm(request.POST)
    if form.is_valid():
      wishlist = form.save(commit = False)
      wishlist.owner = request.user
      wishlist.title = form.cleaned_data['title']
      wishlist.save()
      return HttpResponseRedirect(reverse('wish_home'))
  else:
    pass

def listWishlist(request):
  wishlists = Wishlist.objects.filter(owner=request.user)

  return render_to_response('wish/list_wishlist.html', {'wishlists':wishlists}, context_instance=RequestContext(request))

def listWish(request, wishlist_id=0):
  wish_list = Wish.objects.filter(related_list__id=wishlist_id)

  return render_to_response('wish/list_wish.html', {'wish_list':wish_list, 'wishlist_id': wishlist_id}, context_instance=RequestContext(request))

def listWishCategory(request):
  wish_category_list = WishCategory.objects.filter(is_approved=True)

  return render_to_response('wish/list_wishcategory.html', {'wish_category_list':wish_category_list}, context_instance=RequestContext(request))
