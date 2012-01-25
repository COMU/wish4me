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
  if FriendshipInvitation.objects.filter(from_user=user_that_invites, to_user=friend_to_invite).exclude(status__in=[3,4,5]).count() > 0:
    print "You have invited that user already"
  elif FriendshipInvitation.objects.filter(from_user=friend_to_invite, to_user=user_that_invites).exclude(status__in=[3,4,5]).count() > 0:
    print "This user has invited you, Y U NO ACCEPT"
  else:
    friend_invitation = FriendshipInvitation(from_user=user_that_invites, to_user=friend_to_invite)
    friend_invitation.save()
  return HttpResponseRedirect(reverse("homePage"))
