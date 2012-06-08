from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from friend.utils import getCommonFriendCount
from wish4meUI.friend.models import *

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
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def follow_multiple_users(request):
  my_follow_list = request.POST.getlist('my_follow_list')
  for following_user_id in my_follow_list:
    user_to_follow = User.objects.get(pk = following_user_id)
    user_following = request.user;
    if user_to_follow == user_following:
      print "you cannot follow yourself"
    elif Following.objects.filter(from_user=user_following, to_user=user_to_follow, is_hidden = False).count() > 0:
      print "You are following that user already"
    else:
      following = Following(from_user=user_following, to_user=user_to_follow)
      following.save()
  return HttpResponseRedirect(reverse("homePage"))

@login_required
def listFriends(request):
  following_user = request.user
  followers = Following.objects.filter(to_user=following_user, is_hidden = False)
  followers_list = []
  for follower in followers:
    profile = follower.from_user.get_profile()
    if Following.objects.filter(from_user = following_user, to_user=profile.user).count() > 0:
      profile.is_following=True
    else:
      if FriendshipInvitation.objects.filter(from_user = follower.from_user, to_user=following_user, status = "1").count() > 0:
        invite = FriendshipInvitation.objects.get(from_user = follower.from_user, to_user=following_user, status = "1")
        profile.invite = invite.id
        profile.is_followed = True
    profile.common_count = getCommonFriendCount(request, follower.from_user)
    followers_list.append(profile)

  followings = Following.objects.filter(from_user=following_user, is_hidden = False)
  followings_list = []
  for following in followings:
    profile = following.to_user.get_profile()
    profile.common_count = getCommonFriendCount(request, following.from_user)
    profile.is_following=True
    followings_list.append(profile)

  return render_to_response('friend/friends.html', {'followers_list': followers_list, 'followings_list' : followings_list,  'page_title': 'List followers'}, context_instance=RequestContext(request))

@login_required
def acceptInvite(request, invite_id):
  invite = get_object_or_404(FriendshipInvitation, pk = invite_id)
  invite.accept()
  return   HttpResponseRedirect(reverse("list_friends"))
  return render_to_response('friend/followers.html', {'followers_list': followers_list, 'page_title': 'List Friends'}, context_instance=RequestContext(request))

@login_required
def acceptInvite(request, invite_id):
  invite = get_object_or_404(FriendshipInvitation, pk = invite_id)
  invite.accept()
  return   HttpResponseRedirect(reverse("list_friends"))
