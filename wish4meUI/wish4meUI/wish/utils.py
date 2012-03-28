from wish4meUI.wish.models import Wish, WishAccomplish

def addAccomplishesToWishes(wishes):
  for wish in wishes:
    accomplishes = WishAccomplish.objects.filter(wish=wish)
    wish.accomplishes = accomplishes
