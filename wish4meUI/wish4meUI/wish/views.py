#! -*- coding: utf-8 -*-
# Create your views here.
from django.core.files.base import ContentFile

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,\
  HttpResponseForbidden
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
from random import randint
import urllib2
from urlparse import urlparse

from wish4meUI.wish.forms import WishForm, WishCategoryForm, WishPhotoForm, AccomplishForm, WishLocationForm
from wish4meUI.wish.models import Wish, WishCategory, WishPhoto, WishAccomplish, WishLocation
from wish4meUI.friend.models import Following
from wish4meUI.wishlist.models import Wishlist
from wish4meUI.wish.utils import addAccomplishesToWishes

from django.conf import settings
import urllib, urllib2, json, datetime, simplejson

def myActivity(request):
  wishes = Wish.objects.filter(related_list__owner=request.user, is_hidden=False).order_by("-request_date")
  addAccomplishesToWishes(wishes)

  activity_state = None

  if not len(wishes):
    activity_state = 'images/noWish_%s.jpg' % randint(1,1)

  paginator = Paginator(wishes, 25)
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    wishes = paginator.page(page)
  except (EmptyPage, InvalidPage):
    wishes = paginator.page(paginator.num_pages)

  context = {'wishes': wishes.object_list, 'paginator_objects': wishes,
             'page_title': "My wish activity", 'activity_state': activity_state}
  return render_to_response('wish/activity.html', context, context_instance=RequestContext(request))

def specificFriendActivity(request, friend_id):
  friend = get_object_or_404(User, id=friend_id)
  if friend == request.user:
    return HttpResponseRedirect(reverse("my-activity"))
  
  are_friends = Following.objects.areFriends(request.user, friend)
  if are_friends or True:
      
    wishes = Wish.objects.filter(related_list__owner = friend, is_hidden = False, is_private=False)
    wishes = wishes.order_by("-request_date")[:5]
    addAccomplishesToWishes(wishes)
    #wishes = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False).order_by("-request_date")[:5]
  
    paginator = Paginator(wishes, 25)
    try:
      page = int(request.GET.get('page', '1'))
    except ValueError:
      page = 1
  
    try:
      wishes = paginator.page(page)
    except (EmptyPage, InvalidPage):
      wishes = paginator.page(paginator.num_pages)
  
    context = {'wishes': wishes.object_list,
               'page_title': 'Friend activity',
               'dont_show_add_wish_button': True,
               'paginator_objects': wishes}
    return render_to_response("wish/activity.html", context, context_instance=RequestContext(request))
  else:
    return HttpResponseForbidden("Not allowed")
  
  
def friendActivity(request):
  following_list = Following.objects.filter(from_user = request.user).values('to_user_id')
  friends_list = Following.objects.filter(from_user__in = following_list, to_user = request.user).values('from_user_id')

  #print(str(Wish.objects.filter(related_list__owner__in = following_list).query))
  wishes_from_friends = Wish.objects.filter(related_list__owner__in = friends_list, is_hidden = False)
  wishes_from_following = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False, is_private = False)
  wishes = wishes_from_friends | wishes_from_following
  wishes = wishes.order_by("-request_date")[:5]
  addAccomplishesToWishes(wishes)
  #wishes = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False).order_by("-request_date")[:5]

  activity_state = None

  if not len(friends_list) and not len(following_list):
    activity_state = 'images/noFriend_%s.jpg' % randint(1,2)

  if not len(wishes_from_following) and not len(wishes_from_friends) and not activity_state:
    activity_state = 'images/noFriendWish_%s.jpg' % randint(1,1)

  paginator = Paginator(wishes, 25)
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    wishes = paginator.page(page)
  except (EmptyPage, InvalidPage):
    wishes = paginator.page(paginator.num_pages)

  context = {'wishes': wishes.object_list,
             'page_title': 'Friend activity',
             'paginator_objects': wishes, 'activity_state': activity_state}
  return render_to_response("wish/activity.html", context, context_instance=RequestContext(request))

def add_to_my_wishes(request, wish_id):
	orig_wish = get_object_or_404(Wish, pk=wish_id)

	new_wish = orig_wish

	new_wish.pk = None
	new_wish.related_list = Wishlist.objects.filter(owner=request.user)[0]
	new_wish.wish_for = request.user

	new_wish.save()

	return HttpResponseRedirect(reverse('my-activity'))

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
      wish.request_date = datetime.datetime.now()

      # get the location details from Foursquare
      location_id = request.POST.get('location', False)
      if location_id:
        # https://api.foursquare.com/v2/venues/40a55d80f964a52020f31ee3?oauth_token=AK5N2LRQLI5ELG25THGKETHDFEPY2LXNTANXFJIHEJWWQRRS&v=20120504
        oauth_token = settings.LOCATION_SEARCH_OAUTH_TOKEN
        url = "https://api.foursquare.com/v2/venues"
        now = datetime.datetime.now()
        v = now.strftime("%Y%m%d")
        oauth_string = "=".join(["oauth_token", oauth_token])
        date_string = "=".join(["v", v])
        foursquare_api_url = "/".join([url, "/", location_id]) + "?" + "&".join([oauth_string, date_string])
        response = urllib2.urlopen(foursquare_api_url)
        response = response.read()
        result = json.loads(response)
        venue = result['response']['venue']
        name = venue['name']
        location = venue['location']
        if location.has_key('address'):
            address = location['address']
        else:
            address = None
        if location.has_key('lat'):
            latitude = location['lat']
        else:
            latitude = None
        if location.has_key('lng'):
            longitude = location['lng']
        else:
            longitude = None
        if location.has_key('city'):
            city = location['city']
        else:
            city = None
        if location.has_key('state'):
            state = location['state']
        else:
            state = None
        if location.has_key('country'):
            country = location['country']
        else:
            country = None

        wish_location, created = WishLocation.objects.get_or_create(name=name, address=address, latitude=latitude, longitude=longitude, city=city, state=state, country=country)
        wish.location = wish_location
      wish.save()
      for photoform in wish_photo_set_form.forms:
          photo = photoform.save(commit = False)
          try:
              if photo.photo:
                photo.wish = wish
                photo.save()
              elif photoform.cleaned_data['url'] != '':
                photo.wish = wish
                photo_name = urlparse(photoform.cleaned_data['url']).path.split('/')[-1]
                photo_content = ContentFile(urllib2.urlopen(photoform.cleaned_data['url']).read())
                photo.photo.save(photo_name, photo_content, save=False)
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
  people_to_list = (followers & followed) | users_self
  #Bootstrap typeahead is pretty strict, creating list in here is much cleaner.
  typeahead_source = "["
  for friend in people_to_list:
    typeahead_source += "\"" + friend.username + "\","
  typeahead_source = typeahead_source[:-1]
  typeahead_source += "]"
  #friends_list = people_to_list.values('username')
  wish_form.fields['wish_for_text'].widget.attrs['data-source'] = typeahead_source

  context = {'typeahead_source': typeahead_source,
             'page_title': 'Add wish',
             'form': wish_form,
             'wish_photo_set_form': wish_photo_set_form}
  return render_to_response('wish/add.html', context, context_instance=RequestContext(request))


def edit(request, wish_id):
	_wish = Wish.objects.get(pk=wish_id)
	WishPhotoSet = formset_factory(WishPhotoForm, extra=5, max_num=5)
	if request.POST:
		wish_form = WishForm(request.user, request.POST, prefix=WishForm.__class__.__name__)
		wish_photo_set_form = WishPhotoSet(request.POST, request.FILES, prefix=WishPhotoSet.__class__.__name__)
		if wish_form.is_valid():
			wish = get_object_or_404(Wish, pk=wish_id)
			wish_for = wish_form.cleaned_data['wish_for_text']
			wish.wish_for = User.objects.get(username = wish_for)
			wish.description = wish_form.cleaned_data['description']
			wish.name = wish_form.cleaned_data['name']
			wish.brand = wish_form.cleaned_data['brand']
			wish.category = wish_form.cleaned_data['category']
			wish.related_list = wish_form.cleaned_data['related_list']
			wish.save()

			lc = 0
			lc_1 = 0
			wpl = WishPhoto.objects.filter(wish=_wish, is_hidden=False)
			for photoform in wish_photo_set_form.forms:
				try:
					if request.POST['remove_photo_%s' % lc_1] == 'on':
						wp = wpl[lc]
						wp.is_hidden = True
						wp.save()
						lc_1 += 1
						continue
				except:
					pass

				photo = photoform.save(commit = False)
				try:

					if photo.photo:
						try:
							wp = wpl[lc]
							wp.is_hidden = True
							wp.save()
							lc -= 1
						except:
							pass

						photo.wish = wish
						photo.save()



					elif photoform.cleaned_data['url'] != '':


						photo.wish = wish
						photo_name = urlparse(photoform.cleaned_data['url']).path.split('/')[-1]
						photo_content = ContentFile(urllib2.urlopen(photoform.cleaned_data['url']).read())
						try:
							wp = wpl[lc]
							wp.is_hidden = True
							wp.save()
							lc -= 1
						except:
							pass
						photo.photo.save(photo_name, photo_content, save=False)
						photo.save()




				except:
					pass

				lc += 1
				lc_1 += 1

		return HttpResponseRedirect(reverse('my-activity'))
	else:


		follower_relation = Following.objects.filter(to_user = request.user, is_hidden = False).values('from_user')
		followers = User.objects.filter(id__in = follower_relation)
		followed_relation = Following.objects.filter(from_user = request.user, is_hidden = False).values('to_user')
		followed = User.objects.filter(id__in = followed_relation)
		users_self = User.objects.filter(id = request.user.id)
		people_to_list = (followers & followed) | users_self
		#Bootstrap typeahead is pretty strict, creating list in here is much cleaner.
		typeahead_source = "["
		for friend in people_to_list:
			typeahead_source += "\"" + friend.username + "\","
		typeahead_source = typeahead_source[:-1]
		typeahead_source += "]"
		#friends_list = people_to_list.values('username')


		wish_form = WishForm(request.user, instance = _wish, prefix=WishForm.__class__.__name__)
		wish_form.fields['wish_for_text'].widget.attrs['data-source'] = typeahead_source
		wish_photo_set_form = WishPhotoSet(prefix=WishPhotoSet.__class__.__name__)

		photos = WishPhoto.objects.filter(wish=_wish, is_hidden=False)

		details = { 'form': wish_form, 'wish_photo_set_form': wish_photo_set_form, 'photos': photos,
		            'page_title': 'Edit wish', 'typeahead_source': typeahead_source, 'wish_id': wish_id,}
		return render_to_response('wish/edit.html', details, context_instance=RequestContext(request))


def show(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  return render_to_response('wish/wish.html',
                            {'wish': wish, 'page_title': "What i wish is ... "},
                            context_instance=RequestContext(request))


def remove(request, wish_id):
  wish = get_object_or_404(Wish, pk=wish_id)
  wish.is_hidden = True
  wish.save()

  return HttpResponseRedirect(reverse('wishlist-home'))

def changeStatus(request, wish_id):
  pass


def listAllWishes(request):
  wish_list = Wish.objects.filter(related_list__owner=request.user, is_hidden=False)
  addAccomplishesToWishes(wish_list)
  return render_to_response('wish/list_wishes.html',
                            {'wish_list': wish_list, 'wishlist_id': 1,
                             'page_title': 'List all wishes'},
                            context_instance=RequestContext(request))

def list(request, wishlist_id=0):
  wishes = Wish.objects.filter(related_list__owner=request.user, related_list__id=wishlist_id, is_hidden=False).order_by("-request_date")
  addAccomplishesToWishes(wishes)
  wishlist = Wishlist.objects.get(pk = wishlist_id)
  title = "Wishes in \"" + wishlist.title + "\" list"
  return render_to_response('wish/activity.html', {'wishes': wishes, 'page_title': title}, context_instance=RequestContext(request))

def addWishCategory(request):
  wishcategory = WishCategory(name="Default", is_approved=True, is_hidden=False)
  wishcategory.save()

  return HttpResponseRedirect(reverse('wish_home'))


def listWishCategory(request):
  wish_category_list = WishCategory.objects.filter(is_approved=True, is_hidden=False)

  return render_to_response('wish/list_wishcategory.html',
                            {'wish_category_list':wish_category_list, 'page_title': 'List wish category'},
                            context_instance=RequestContext(request))

def showWishAlone(request, wish_id):
  wish = get_object_or_404(Wish, is_hidden = False,  pk = wish_id)
  addAccomplishesToWishes(wish)
  photos = WishPhoto.objects.filter(is_hidden = False, wish__id = wish_id)

  return render_to_response('wish/show_wish_alone.html',
                            {'wish': wish, 'photos': photos, 'page_title': 'Show wish'},
                            context_instance=RequestContext(request))

def accomplish(request, wish_id):
  wish = get_object_or_404(Wish, is_hidden = False,  pk = wish_id)
  if request.POST:
    accomplishForm = AccomplishForm(request.POST)
    if accomplishForm.is_valid():
      accomplish = accomplishForm.save(commit=False)
      accomplish.accomplisher = request.user
      accomplish.wish = wish
      print accomplish
      accomplish.save()
      print "saved"
      return HttpResponseRedirect(reverse('show-wish', args=[wish_id]))
    else:
      return HttpResponse('Accomplish Form is not valid')
  else:
    accomplishForm = AccomplishForm()
    return render_to_response('wish/accomplish.html',
                            {'form': accomplishForm,'wish' : wish, 'page_title': 'Accomplish wish'},
                            context_instance=RequestContext(request))

def respondAccomplish(request, accomplish_id, response):
  accomplish = get_object_or_404(WishAccomplish,  pk = accomplish_id)
  if response == "accept":
    accomplish.status = 2
    accomplish.wish.is_accomplished = True
    accomplish.wish.accomplish_date = datetime.now()
    accomplish.wish.save()
  if response == "decline":
    accomplish.status = 3
  accomplish.save()
  return HttpResponseRedirect(reverse('show-wish', args=[accomplish.wish.id]))


def getLocations(request):
	#print "get location is called"
	#location operations
	city = request.POST.get('city', False)
	location_address = urllib.quote(city.encode("utf-8"))
	#sending to the google_maps api to get the latitude and longitude
	google_api_url = "".join(["http://maps.googleapis.com/maps/api/geocode/json?address=",location_address,"&sensor=false"])
	response = urllib2.urlopen(google_api_url)
	response = response.read()
	result = json.loads(response)['results'][0]
	geometry = result['geometry']['location']
	latitude = geometry['lat']
	longitude = geometry['lng']
	# get the the environments aroun the location
	oauth_token = settings.LOCATION_SEARCH_OAUTH_TOKEN
	#print "oauth token:", oauth_token
	now = datetime.datetime.now()
	v = now.strftime("%Y%m%d")
	foursquare_api_url = "".join(["https://api.foursquare.com/v2/", "venues/search?ll=", ",".join([str(latitude),str(longitude)]),"&oauth_token=", oauth_token, "&v=", v, "&intent=checkin"])
	#print "foursquare url called:", foursquare_api_url
	response = urllib2.urlopen(foursquare_api_url)
	response = response.read()
	result = json.loads(response)
	venues = result['response']['venues']
	response_data = []
	for venue in venues:
		#keys
		#[u'verified',
		#  u'name',
		#  u'hereNow',
		#  u'specials',
		#  u'contact',
		#  u'location',
		#  u'stats',
		#  u'id',
		#  u'categories']
		name = venue['name']
		id = venue['id']
		#location = venue['location']
		#example location output
		#{u'address': u'180 Maiden Lane',
		#  u'city': u'New York',
		#  u'country': u'United States',
		#  u'crossStreet': u'Water Street',
		#  u'distance': 36,
		#  u'lat': 40.70019871930678,
		#  u'lng': -73.99964860547712,
		#  u'postalCode': u'10038',
		#  u'state': u'NY'}
		response_data.append((id,name))
	print response_data
	return HttpResponse(json.dumps(response_data), mimetype="application/json")

def addLocation(request):
	if request.method == "POST":
		form = WishLocationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('''
                    <script type="text/javascript">
                            opener.dismissAddAnotherPopup(window);
                    </script>'''
			)
	else:
		form = WishLocationForm()
	return render_to_response('wish/add_location.html',
			{'form': form, 'page_title': 'Add a new location'},
		context_instance=RequestContext(request))

def searchLocation(request):
	results = []
	print "searchLocation called"
	if request.method == "GET":
		if request.GET.has_key(u'q'):
			value = request.GET[u'q']
			# Ignore queries shorter than length 3
			if len(value) > 2:
				model_results = WishLocation.objects.filter(name__icontains=value)
				results = [ (x.__unicode__(), x.id) for x in model_results ]
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')

