from django.template.context import RequestContext
from django.shortcuts import render_to_response
from contact_importer.utils import *
from django.contrib.auth.decorators import login_required

@login_required
def contact_importer_home(request, importing_profile=0):
      user = request.user
      profile = user.get_profile()
      friends_list = ""
      print profile.facebook_profile and True or False
      if importing_profile == 'facebook':
        if profile.facebook_profile and True or False==True:
          friends_list = facebook_contact_import(request)
      elif importing_profile == 'foursquare':
        if profile.foursq_profile and True or False==True:
          friends_list = foursquare_contact_import(request)
      elif importing_profile == 'twitter':
        if profile.twitter_profile and True or False==True:
          friends_list = twitter_contact_import(request)
      elif importing_profile == 'google':
        if profile.google_profile and True or False==True:
          friends_list = google_contact_import(request)
      context = {
      'user' : user,
      'profile': user.get_profile(),
      'page_title': 'Import Contacts',
      'facebook_profile_activated': profile.facebook_profile and True or False,
      'google_profile_activated': profile.google_profile and True or False,
      'twitter_profile_activated': profile.twitter_profile and True or False,
      'foursq_profile_activated': profile.foursq_profile and True or False,
      'imported_friends' : friends_list
      }

      return render_to_response('contact_importer/home.html', context,  context_instance=RequestContext(request, ))
