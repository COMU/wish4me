#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

from datetime import datetime

from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishlistForm, WishPhotoForm
from wish4meUI.wish.models import Wish, WishCategory, Wishlist, WishPhoto

def homeWish(request):
  wishlists = Wishlist.objects.filter(owner=request.user, is_hidden=False)
  wishlist_form = WishlistForm()

  return render_to_response('wish/wish.html', {'wishlists':wishlists, 'wishlist_form': wishlist_form}, context_instance=RequestContext(request))

def addWish(request, wishlist_id):
  wish_photo_set = formset_factory(WishPhotoForm, extra=5, max_num=5)
  if request.POST:
    form = WishForm(request.POST, prefix='wishform')
    wish_photo_set_form = wish_photo_set(request.POST, request.FILES, prefix='photoform')
    if form.is_valid():
      wish = form.save(commit = False)
      wish.wish_for = request.user
      wish.description = form.cleaned_data['description']
      wish.name = form.cleaned_data['name']
      wish.brand = form.cleaned_data['brand']
      wish.category = form.cleaned_data['category']
      print "hede"
      print wish_photo_set_form
      wish.request_date = datetime.now()
      wish.related_list = Wishlist.objects.get(pk=wishlist_id)
      wish.save()
      
      try:
        for photoform in wish_photo_set_form.forms:
          photo = photoform.save(commit = False)
          if photo.photo:
            photo.wish = wish
            photo.save()
      except:
        pass


      return HttpResponseRedirect(reverse('wish_list_wish', args=[wishlist_id]))
    else:
      print form.errors
  else:
    wish_form = WishForm(prefix='wishform')
    wish_photo_set_form = wish_photo_set(prefix='photoform')

    return render_to_response('wish/add_wish.html', {'wish_form': wish_form, 'wishlist_id': wishlist_id, 'wish_photo_set_form': wish_photo_set_form}, context_instance=RequestContext(request))

def editWish(request, wish_id):
  return HttpResponseRedirect(reverse('wish_home'))

def removeWish(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  wish.is_hidden = True
  wish.save()

  return HttpResponseRedirect(reverse('wish_list_wish', args=[wish.related_list.id]))


def accomplishWish(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  if wish.accomplish_date is None:
    wish.accomplish_date = datetime.now()
  else:
    wish.accomplish_date = None
  wish.save()

  return HttpResponseRedirect(reverse('wish_list_wish', args=[wish.related_list.id]))


def listAllWishes(request):
  wish_list = Wish.objects.filter(related_list__owner=request.user, is_hidden=False)

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
  wishlists = Wishlist.objects.filter(owner=request.user, is_hidden=False)

  return render_to_response('wish/list_wishlist.html', {'wishlists':wishlists}, context_instance=RequestContext(request))

def editWishlist(request, wishlist_id=0):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
  form = WishlistForm()
  form.title = wishlist.title
  form.id = wishlist.id
  form.owner = wishlist.owner
  form.is_hidden = wishlist.is_hidden
  wishlists = Wishlist.objects.filter(owner=request.user)

  return render_to_response('wish/list_wishlist.html', {'wishlists':wishlists}, context_instance=RequestContext(request))

def removeWishlist(request, wishlist_id):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
  wishlist.is_hidden = True
  wishlist.save()

  return HttpResponseRedirect(reverse('wish_home'))

def listWish(request, wishlist_id=0):
  wish_list = Wish.objects.filter(related_list__id=wishlist_id, is_hidden=False)

  return render_to_response('wish/list_wish.html', {'wish_list':wish_list, 'wishlist_id': wishlist_id}, context_instance=RequestContext(request))

def addWishCategory(request):
  wishcategory = WishCategory(name="Default", is_approved=True, is_hidden=False)
  wishcategory.save()

  return HttpResponseRedirect(reverse('wish_home'))


def listWishCategory(request):
  wish_category_list = WishCategory.objects.filter(is_approved=True, is_hidden=False)

  return render_to_response('wish/list_wishcategory.html', {'wish_category_list':wish_category_list}, context_instance=RequestContext(request))
