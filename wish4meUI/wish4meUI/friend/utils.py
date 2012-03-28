from wish4meUI.friend.models import Following
from wish4meUI.wish.models import Wish

def getFollowingWishes(request):
  following_list = Following.objects.filter(from_user = request.user).values('to_user_id')
  friends_list = Following.objects.filter(from_user__in = following_list, to_user = request.user).values('from_user_id')
    
  #print(str(Wish.objects.filter(related_list__owner__in = following_list).query))
  wishes_from_friends = Wish.objects.filter(related_list__owner__in = friends_list, is_hidden = False)
  wishes_from_following = Wish.objects.filter(related_list__owner__in = following_list, is_hidden = False, is_private = False)
  wishes = wishes_from_friends | wishes_from_following
  return wishes

def getCommonFriendCount(request, friend_id):
  user_follower = Following.objects.filter(from_user = request.user, is_hidden = False)
  user_followed = Following.objects.filter(to_user = request.user, is_hidden = False)

  _this_friendship = Following.objects.filter(from_user = request.user, to_user = friend_id, is_hidden = False)

  if len(_this_friendship) == 0:
    _this_friendship = Following.objects.filter(from_user = friend_id, to_user = request.user, is_hidden = False)

  if len(_this_friendship) != 0:
    this_friendship = _this_friendship[0]

  user_followers = user_follower | user_followed

  if len(_this_friendship) != 0:
    user_followers = user_followers.exclude(pk = this_friendship.id)

  friend_follower = Following.objects.filter(from_user = friend_id, is_hidden = False)
  friend_followed = Following.objects.filter(to_user = friend_id, is_hidden = False)

  friend_followers = friend_follower | friend_followed

  if len(_this_friendship) != 0:
    friend_followers = friend_followers.exclude(pk = this_friendship.id)

  common_friends = []


  for user_follow in user_followers:
    if user_follow.from_user == request.user:
      _user = user_follow.to_user
    else:
      _user = user_follow.from_user

    for friend_follow in friend_followers:
      if friend_follow.from_user == friend_id:
        _friend = friend_follow.to_user
      else:
        _friend = friend_follow.from_user
      if user_follow.from_user.get_profile().is_private == True:
        if user_follow.to_user == request.user and _user == _friend:
          common_friends.append(user_follow)
      if _user == _friend:
        common_friends.append(user_follow)

  return len(common_friends)

        

    
  
  
