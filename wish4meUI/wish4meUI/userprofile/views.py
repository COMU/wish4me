from userprofile.models import *
from django.contrib.auth.models import User
from django.http import *
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from itertools import chain

from userprofile.forms import UserSearchForm, UserInformationForm
from wish4meUI.friend.utils import getFollowingWishes
from wish4meUI.wish.models import Wish
from friend.models import Following, FriendshipInvitation
from django.conf import settings

@login_required
def userLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def userProfile(request):
    user = request.user
    profile = user.get_profile()

    context = {
        'user' : user,
        'profile': user.get_profile(),
        'page_title': 'User details'
    }
    return render_to_response('userprofile/profile.html', context, context_instance=RequestContext(request))

@login_required
def userInformationEdit(request):
    user = request.user
    profile = user.get_profile()

    context = {
      'facebook_profile_activated': profile.facebook_profile and True or False,
      'google_profile_activated': profile.google_profile and True or False,
      'twitter_profile_activated': profile.twitter_profile and True or False,
      'foursq_profile_activated': profile.foursq_profile and True or False,
    }

    if request.method == 'POST':
        form = UserInformationForm(request.POST, instance=user)
        if form.is_valid():
            if request.FILES.has_key('photo'):
                img = request.FILES['photo']
                profile = user.get_profile()
                profile.photo.save(img.name, img)
            gender = request.POST.get('gender')
            profile.gender = gender
            is_private = request.POST.get('is_private')
            profile.is_private = is_private
            profile.save()
            form.save()
    else:
        form = UserInformationForm(initial = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'gender': profile.gender})

    userDetails = { 'user' : user, 'profile': profile, 'form': form,
                    'page_title': 'Edit profile'}
    context.update(userDetails)
    return render_to_response('userprofile/edit_information.html', context, context_instance=RequestContext(request))

@login_required
def userLoginSuccess(request):
  return render_to_response('userprofile/loginSuccess.html', context_instance=RequestContext(request))

@login_required
def userLoginFail(request):
  return render_to_response('userprofile/login_failed.html', context_instance=RequestContext(request))

def userListAll(request):
  all_users = UserProfile.objects.all()
  return render_to_response('userprofile/list_all.html', {'all_users': all_users}, context_instance=RequestContext(request))

def userSearch(request):
  if request.POST:
    form = UserSearchForm(request.POST.copy())
    if form.is_valid():
      term = form.cleaned_data['search_query']
      #search for users #
      users_query = User.objects.filter(Q(username__icontains = term) |
                                        Q(first_name__icontains = term) |
                                        Q(last_name__icontains = term)).distinct()
      users_query = users_query.exclude(pk = request.user.id)
      users_list = []
      for user in users_query:
        try:
          profile = user.get_profile()
          profile.is_following = Following.objects.filter(from_user=request.user, to_user=user).count() > 0
          profile.is_followed = FriendshipInvitation.objects.filter(from_user=user, to_user=request.user).count() > 0
          if profile.is_followed:
            invite = FriendshipInvitation.objects.get(from_user=user, to_user=request.user)
            if invite.status == "1":
              profile.invite = invite.id
          users_list.append(profile)
        except ObjectDoesNotExist:
          pass                                  #TODO better handling for admin needed, but this works for now.
      # End Search for users #
      # search for wishes #
      my_wishes = Wish.objects.filter(related_list__owner = request.user, is_hidden = False)
      wishes = getFollowingWishes(request) | my_wishes
      wishes = wishes.filter(Q(wish_for__username__icontains = term) |
                             Q(description__icontains = term) |
                             Q(brand__icontains = term) |
                             Q(name__icontains = term))
      return render_to_response('userprofile/search.html', {'page_title': 'Search user', 'users_list': users_list, 'wishes' :wishes}, context_instance=RequestContext(request))
    else:
      print "userprofile.userSearch: form is invalid"
      #return HttpResponse("userprofile.userSearch: form is invalid")
      search_form = UserSearchForm()
      return render_to_response('userprofile/search.html', {'page_title': 'Search user', 'form' : search_form, }, context_instance=RequestContext(request))
  else:
    return HttpResponse("userprofile.userSearch: the request does not contain POST")

