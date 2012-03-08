# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.contrib import messages

from wish4meUI.wishlist.forms import WishlistForm
from wish4meUI.wishlist.models import Wishlist

def add(request):
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

def myWishlists(request):
  wishlists = Wishlist.objects.filter(owner = request.user, is_hidden = False)
  
  return render_to_response('wishlist/myWishlists.html', {'wishlists': wishlists}, context_instance=RequestContext(request))

def show(request, wishlist_id=0):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)

  return render_to_response('wishlist/show.html', {'wishlist': wishlist}, context_instance=RequestContext(request))

def edit(request, wishlist_id=0):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
  form = WishlistForm()
  form.title = wishlist.title
  form.id = wishlist.id
  form.owner = wishlist.owner
  form.is_hidden = wishlist.is_hidden
  wishlists = Wishlist.objects.filter(owner=request.user)

  return render_to_response('wishlist/list_wishlist.html', {'wishlists':wishlists}, context_instance=RequestContext(request))

def remove(request, wishlist_id):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
  wishlist.is_hidden = True
  wishlist.save()

  return HttpREsponseRedirect(reverse('wish_home'))
