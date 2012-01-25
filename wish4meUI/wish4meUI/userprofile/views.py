from userprofile.models import *
from django.contrib.auth.models import User
from django.http import *
from twitter_app.views import *
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def userLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def userProfile(request):
  userDetails = { 'name' : request.user.username }
  return render_to_response('userprofile/profile.html', {'userDetails': userDetails}, context_instance=RequestContext(request))


@login_required
def userLoginSuccess(request):
  return render_to_response('userprofile/loginSuccess.html', context_instance=RequestContext(request))

@login_required
def userLoginFail(request):
  return render_to_response('userprofile/login_failed.html', context_instance=RequestContext(request))

def userListAll(request):
  all_users = UserProfile.objects.all()
  return render_to_response('userprofile/list_all.html', {'all_users': all_users}, context_instance=RequestContext(request))

