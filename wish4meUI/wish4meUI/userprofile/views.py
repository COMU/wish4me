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
from friend.models import Following, FriendshipInvitation
from django.conf import settings

@login_required
def userLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def userProfile(request):
    user = request.user
    userDetails = { 'user' : user, 'profile': user.get_profile()}
    return render_to_response('userprofile/profile.html', userDetails, context_instance=RequestContext(request))

@login_required
def userInformationEdit(request):
    user = request.user
    profile = user.get_profile()
    if request.method == 'POST':
        form = UserInformationForm(request.POST, instance=user)
        if form.is_valid():
            if request.FILES.has_key('photo'):
                img = request.FILES['photo']
                profile = user.get_profile()
                profile.photo.save(img.name, img)
            gender = request.POST.get('gender')
            profile.gender = gender
            profile.save()
            form.save()
    else:
        form = UserInformationForm(initial = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'gender': profile.gender})

    userDetails = { 'user' : user, 'profile': profile, 'form': form }
    return render_to_response('userprofile/edit_information.html', userDetails, context_instance=RequestContext(request))

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
      users_query = User.objects.filter(Q(username__icontains = term) |
                                      Q(first_name__icontains = term) |
                                      Q(last_name__icontains = term)).distinct()
      users_query = users_query.exclude(pk = request.user.id)
      users_list = []
      for user in users_query:
        try:
          profile = user.get_profile()
          profile.is_following = Following.objects.filter(from_user=request.user, to_user=user).count() > 0
          print "following " ,profile.is_following
          profile.is_followed = FriendshipInvitation.objects.filter(from_user=user, to_user=request.user).count() > 0
          if profile.is_followed:
            invite = FriendshipInvitation.objects.get(from_user=user, to_user=request.user)
            if invite.status == "1":
              profile.invite = invite.id
          users_list.append(profile)
        except ObjectDoesNotExist:
          pass                                  #TODO better handling for admin needed, but this works for now.
      return render_to_response('userprofile/search.html', {'users_list': users_list}, context_instance=RequestContext(request))
    else:
      print "userprofile.userSearch: form is invalid"
      #return HttpResponse("userprofile.userSearch: form is invalid")
      search_form = UserSearchForm()
      return render_to_response('userprofile/search.html', {'form' : search_form, }, context_instance=RequestContext(request))
  else:
    return HttpResponse("userprofile.userSearch: the request does not contain POST")

