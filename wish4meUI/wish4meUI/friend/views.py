from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from friend.models import *

@login_required
def invite(request,friend_id):
  friend_to_invite = User.objects.get(pk = friend_id)
  user_that_invites = request.user;
  if Friendship.objects.filter(from_user=user_that_invites, to_user=friend_to_invite).count() > 0:
    print "You are following that user already"
  else:
    friendship = Friendship(from_user=user_that_invites, to_user=friend_to_invite)
    friendship.save()
  return HttpResponseRedirect(reverse("homePage"))
