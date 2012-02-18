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

from userprofile.forms import UserSearchForm, UserInformationForm
from django.core.files.base import ContentFile
from itertools import chain

@login_required
def userLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def userProfile(request):
  userDetails = { 'name' : request.user.username }
  return render_to_response('userprofile/profile.html', {'userDetails': userDetails}, context_instance=RequestContext(request))

@login_required
def userInformationEdit(request):
    user = request.user
    if request.method == 'POST':
        form = UserInformationForm(request.POST, instance=user)
        if form.is_valid():
            file_content = ContentFile(request.FILES['photo'].read())
            profile = user.get_profile()
            profile.photo.save(request.FILES['photo'].name, file_content)
            form.save()
    else:
        form = UserInformationForm(initial = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})

    userDetails = { 'user' : user, 'form': form }
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
      term = form.cleaned_data['term']
      #TODO if term is blank?
      users_all = User.objects.filter(Q(username__icontains = term) |
                                      Q(first_name__icontains = term) |
                                      Q(last_name__icontains = term)).distinct()
      print len(users_all)
    else:
      print "form is invalid"
      HttpResponse("form is invalid")
  else:
    users_all = -1
    form = UserSearchForm()
  return render_to_response('userprofile/search.html', {'users_all': users_all, 'form': form}, context_instance=RequestContext(request))

