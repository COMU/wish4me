#! -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.models import User

from datetime import datetime

from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishPhotoForm
from wish4meUI.wish.models import Wish, WishCategory, WishPhoto
from wish4meUI.friend.models import Following


def myActivity(request):
  wishes = Wish.objects.filter(related_list__owner=request.user, is_hidden=False).order_by("-request_date")
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
    wish_form = WishForm(request.user, request.POST, prefix=WishForm.__class__.__name__)
    wish_photo_set_form = WishPhotoSet(
        request.POST, request.FILES, prefix=WishPhotoSet.__class__.__name__)
    if wish_form.is_valid():
      wish = wish_form.save(commit = False)
      wish_for = wish_form.cleaned_data['wish_for_text']
      wish.wish_for = User.objects.get(username = wish_for)
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
    wish_form = WishForm(request.user, prefix=WishForm.__class__.__name__)
    wish_photo_set_form = WishPhotoSet(prefix=WishPhotoSet.__class__.__name__)
  follower_relation = Following.objects.filter(to_user = request.user, is_hidden = False).values('from_user')
  followers = User.objects.filter(id__in = follower_relation)
  followed_relation = Following.objects.filter(from_user = request.user, is_hidden = False).values('to_user')
  followed = User.objects.filter(id__in = followed_relation)
  users_self = User.objects.filter(id = request.user.id)
  people_to_list = followers | followed | users_self
  #Bootstrap typeahead is pretty strict, creating list in here is much cleaner.
  typeahead_source = "["
  for friend in people_to_list:
    typeahead_source += "\"" + friend.username + "\","
  typeahead_source = typeahead_source[:-1]
  typeahead_source += "]"
  #friends_list = people_to_list.values('username')
  wish_form.fields['wish_for_text'].widget.attrs['data-source'] = typeahead_source
  return render_to_response('wish/add.html', {'typeahead_source': typeahead_source, 'page_title': 'Add wish', 'form': wish_form, 'wish_photo_set_form': wish_photo_set_form}, context_instance=RequestContext(request))


def edit(request, wish_id):
  return HttpResponseRedirect(reverse('wish_home'))


def show(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  return render_to_response('wish/wish.html', {'wish': wish}, context_instance=RequestContext(request))


def remove(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  wish.is_hidden = True
  wish.save()

  return HttpResponseRedirect(reverse('wishlist-home'))


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
