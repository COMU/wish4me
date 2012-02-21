from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from friend.models import *

@login_required
def follow(request, following_user_id):
  user_to_follow = User.objects.get(pk = following_user_id)
  user_following = request.user;
  if user_to_follow == user_following:
    print "you cannot follow yourself"
  elif Following.objects.filter(from_user=user_following, to_user=user_to_follow, is_hidden = False).count() > 0:
    print "You are following that user already"
  else:
    following = Following(from_user=user_following, to_user=user_to_follow)
    following.save()
  return HttpResponseRedirect(reverse("welcome_page"))

@login_required
def listFollowers(request):
  following_user = request.user
  followers = Following.objects.filter(to_user=following_user, is_hidden = False)
  followers_list = []
  for follower in followers:
    follower_dict = dict()
    follower_dict["username"] = follower.from_user.username
    friendship_invite = FriendshipInvitation.objects.filter(from_user = follower.from_user, to_user=following_user, status = "1")
    if friendship_invite.count() >0:
      follower_dict["invite_id"] = friendship_invite[0].id      #TODO this is a little hackish. fix with try/catch
    else:
      follower_dict["invite_id"] = "-1"      
    followers_list.append(follower_dict)

  return render_to_response('friend/followers.html', {'followers_list': followers_list}, context_instance=RequestContext(request))

@login_required
def acceptInvite(request, invite_id):
  invite = get_object_or_404(FriendshipInvitation, pk = invite_id)
  invite.accept()
  return   HttpResponseRedirect(reverse("friend_followers"))

    
