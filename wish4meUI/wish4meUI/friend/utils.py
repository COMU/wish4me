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
