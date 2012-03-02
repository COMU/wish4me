#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.contrib import messages

from datetime import datetime

from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishlistForm, WishPhotoForm
from wish4meUI.wish.models import Wish, WishCategory, Wishlist, WishPhoto
from wish4meUI.friend.models import Following


def myActivity(request):
  wishes = Wish.objects.filter(related_list__owner=request.user, is_hidden=False)
  return render_to_response('wish/activity.html', {'wishes': wishes}, context_instance=RequestContext(request))


def friendActivity(request):
  following_list = Following.objects.filter(from_user = request.user).values('to_user_id')
  friends_list = Following.objects.filter(from_user__in = following_list, to_user = request.user).values('from_user_id')

  #print(str(Wish.objects.filter(related_list__owner__in = following_list).query))
  wishes_from_friends = Wish.objects.filter(related_list__owner__in = friends_list, is_hidden = False)
  wishes_from_following = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False, is_private = False)
  wishes = wishes_from_friends | wishes_from_following
  wishes = wishes.order_by("-request_date")[:5]
  #wishes = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False).order_by("-request_date")[:5]
  return render_to_response("wish/activity.html", {'wishes' : wishes, }, context_instance=RequestContext(request, {}))


def add(request):
  WishPhotoSet = formset_factory(WishPhotoForm, extra=5, max_num=5)
  if request.POST:
    wish_form = WishForm(request.POST, prefix=WishForm.__class__.__name__)
    wish_photo_set_form = WishPhotoSet(
        request.POST, request.FILES, prefix=WishPhotoSet.__class__.__name__)
    if wish_form.is_valid():
      wish = wish_form.save(commit = False)
      wish.wish_for = request.user
      wish.description = wish_form.cleaned_data['description']
      wish.name = wish_form.cleaned_data['name']
      wish.brand = wish_form.cleaned_data['brand']
      wish.category = wish_form.cleaned_data['category']
      wish.related_list = wish_form.cleaned_data['related_list']
      wish.request_date = datetime.now()
      wish.save()
      try:
        for photoform in wish_photo_set_form.forms:
          photo = photoform.save(commit = False)
          if photo.photo:
            photo.wish = wish
            photo.save()
      except:
        pass

      return HttpResponseRedirect(reverse('my-activity'))
    else:
      messages.add_message(request, messages.ERROR, 'Please correct the errors below.')
  else:
    wish_form = WishForm(prefix=WishForm.__class__.__name__)
    wish_photo_set_form = WishPhotoSet(prefix=WishPhotoSet.__class__.__name__)

  return render_to_response('wish/add.html', {'page_title': 'Add wish', 'form': wish_form, 'wish_photo_set_form': wish_photo_set_form}, context_instance=RequestContext(request))


def edit(request, wish_id):
  return HttpResponseRedirect(reverse('wish_home'))


def show(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  return render_to_response('wish/wish.html', {'wish': wish}, context_instance=RequestContext(request))


def remove(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  wish.is_hidden = True
  wish.save()

  return HttpResponseRedirect(reverse('wish_list_wish', args=[wish.related_list.id]))


def delete(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  if wish.accomplish_date is None:
    wish.accomplish_date = datetime.now()
  else:
    wish.accomplish_date = None
  wish.save()

  return HttpResponseRedirect(reverse('wish_list_wish', args=[wish.related_list.id]))


def changeStatus(request, wish_id):
  pass


def listAllWishes(request):
  wish_list = Wish.objects.filter(related_list__owner=request.user, is_hidden=False)
  return render_to_response('wish/list_wishes.html', {'wish_list': wish_list, 'wishlist_id': 1}, context_instance=RequestContext(request))


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
  for wishlist in wishlists:
    wishes = Wish.objects.filter(related_list=wishlist)
    wishlist.wishes=wishes
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

def renameWishlist(request, wishlist_id):
  if request.POST:
    if request.POST['new_title']:
      new_title = request.POST['new_title']
    else:
      return HttpResponse("wish.renameWisihlist: the request does not contain new name")
    wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
    wishlist.title = new_title
    wishlist.save()
    return HttpResponseRedirect(reverse('wish_list_wishlist'))
  return HttpResponse("wish.renameWisihlist: the request does not contain POST")
  
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

def showWishAlone(request, wish_id):
  wish = get_object_or_404(Wish, is_hidden = False,  pk = wish_id)
  photos = WishPhoto.objects.filter(is_hidden = False, wish__id = wish_id)

  return render_to_response('wish/show_wish_alone.html', {'wish': wish, 'photos': photos}, context_instance=RequestContext(request))
