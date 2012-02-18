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
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', False)
            first_name = request.POST.get('first_name', False)
            last_name = request.POST.get('last_name', False)
            email = request.POST.get('email', False)
            password = request.POST.get('password', False)

            #setting the user information
            #this part should only save the changed value, it can be changed when the ajax is used
            user = request.user

            if password:
                    user.set_password(password)
            if username != user.username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            user.save()
    else:
        form = UserInformationForm(initial = {'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email})

    userDetails = { 'user' : request.user, 'form': form }
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

