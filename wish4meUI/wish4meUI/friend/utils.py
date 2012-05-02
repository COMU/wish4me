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

  _user_followers = user_follower | user_followed

  if len(_this_friendship) != 0:
	  _user_followers = _user_followers.exclude(pk = this_friendship.id)

  user_followers = set()

  for i in _user_followers:
		if i.from_user == request.user:
		  user_followers.add(i.to_user)
		else:
			user_followers.add(i.from_user)

  friend_follower = Following.objects.filter(from_user = friend_id, is_hidden = False)
  friend_followed = Following.objects.filter(to_user = friend_id, is_hidden = False)

  _friend_followers = friend_follower | friend_followed

  if len(_this_friendship) != 0:
	  _friend_followers = _friend_followers.exclude(pk = this_friendship.id)

  friend_followers = set()

  for i in _friend_followers:
		if i.from_user == friend_id:
		  friend_followers.add(i.to_user)
		else:
			friend_followers.add(i.from_user)



  common_friends = []

  for user_follow in user_followers:

    for friend_follow in friend_followers:
      if user_follow.get_profile().is_private == True:
        if user_follow == request.user and user_follow == friend_follow:
          common_friends.append(user_follow)
      if user_follow == friend_follow:
        common_friends.append(user_follow)

  return len(common_friends)

        

    
  
  
