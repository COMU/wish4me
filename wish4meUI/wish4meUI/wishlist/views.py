# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from wish4meUI.wishlist.forms import Wishlist, WishlistForm
from wish4meUI.wish.models import Wish

def addDefaultWishlist(user):
  wishlist = Wishlist()
  wishlist.owner = user
  wishlist.title = "My wishes"
  wishlist.save()
  return wishlist

def add(request):
  if request.POST:
    form = WishlistForm(request.POST)
    if form.is_valid():
      wishlist = form.save(commit = False)
      wishlist.owner = request.user
      wishlist.title = form.cleaned_data['title']
      wishlist.save()
      return HttpResponseRedirect(reverse('wishlist-home'))
  else:
    pass

def myWishlists(request):
  wishlists = Wishlist.objects.filter(owner=request.user, is_hidden=False)
  for wishlist in wishlists:
    wishlist.wish_count = Wish.objects.filter(related_list=wishlist, is_hidden=False).count()
    wishes = Wish.objects.filter(related_list=wishlist, is_hidden=False)
    wishlist.wishes=wishes
  is_last_wishes = False
  if Wishlist.objects.filter(owner = request.user, is_hidden = False).count() < 2:
    is_last_wishes = True

  return render_to_response('wishlist/list_wishlist.html', {'page_title': 'My wishlists', 'wishlists':wishlists, 'is_last_wishes':is_last_wishes},
                                                         context_instance=RequestContext(request))

def show(request, wishlist_id=0):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)

  return render_to_response('wishlist/show.html', {'wishlist': wishlist, 'page_title': 'Wishlist details'}, context_instance=RequestContext(request))

def edit(request, wishlist_id=0):
  wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
  form = WishlistForm()
  form.title = wishlist.title
  form.id = wishlist.id
  form.owner = wishlist.owner
  form.is_hidden = wishlist.is_hidden
  wishlists = Wishlist.objects.filter(owner=request.user)

  return render_to_response('wishlist/list_wishlist.html', {'wishlists':wishlists, 'page_title': 'Edit wishlist'}, context_instance=RequestContext(request))

def remove(request, wishlist_id):
  if request.POST:
    if request.POST['wishlist_id']:
      move_wishlist_id = request.POST['wishlist_id']
      wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
      move_wishlist = get_object_or_404(Wishlist, pk=move_wishlist_id)
      wishes = Wish.objects.filter(related_list=wishlist, is_hidden=False);
      if move_wishlist_id == wishlist_id:
        for wish in wishes:
          wish.is_hidden = True
          wish.save()
      else:	
        for wish in wishes:
	      wish.related_list = move_wishlist
	      wish.save()
      wishlist.is_hidden = True
      wishlist.save()

      return HttpResponseRedirect(reverse('wishlist-home'))
    print("Wislist.views.remove: POST does not contain wishlist_id")
  print("Wislist.views.remove: request does not contain POST")
  return HttpResponseNotFound('<h1>Remove request was invalid</h1>')

def rename(request, wishlist_id):
  if request.POST:
    if request.POST['new_title']:
      new_title = request.POST['new_title']
    else:
      return HttpResponse("wish.renameWisihlist: the request does not contain new name")
    wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
    wishlist.title = new_title
    wishlist.save()
    return HttpResponseRedirect(reverse('wishlist-home'))
  return HttpResponse("wish.renameWisihlist: the request does not contain POST")

@csrf_exempt
def setPrivacy(request, wishlist_id):
  wishlist = Wishlist.objects.get(pk = wishlist_id)
  if wishlist.is_private:
    wishlist.is_private = False
    wishlist.save()
    print "public"
    return HttpResponse("public")
  else:
    wishlist.is_private = True
    wishlist.save()
    print "private"
    return HttpResponse("private")
  

  
