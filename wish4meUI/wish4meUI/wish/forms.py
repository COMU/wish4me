from django import forms
from django.contrib.auth.models import User

from ajax_select import make_ajax_field

from wish4meUI.wish.models import Wish, WishCategory, Wishlist, WishPhoto
from wish4meUI.friend.models import Following

class WishForm(forms.ModelForm):

  def __init__(self, requested_user, *args, **kwargs):
    super(WishForm, self).__init__(*args, **kwargs)

    follower_relation = Following.objects.filter(to_user = requested_user, is_hidden = False).values('from_user')
    followers = User.objects.filter(id__in = follower_relation)
    followed_relation = Following.objects.filter(from_user = requested_user, is_hidden = False).values('to_user')
    followed = User.objects.filter(id__in = followed_relation)
    
    # add your self too
    users_self = User.objects.filter(id = requested_user.id)
    people_to_list = followers | followed | users_self
    self.fields["wish_for"].queryset = people_to_list

  class Meta:
    model = Wish
    exclude = ('request_date', 'accomplish_date', 'is_hidden', )

  #wish_for  = make_ajax_field(User, 'username', 'user-channel', help_text='', label='Wish For')

class WishCategoryForm(forms.ModelForm):
  class Meta:
    model = WishCategory

class WishlistForm(forms.ModelForm):
  class Meta:
    model = Wishlist
    fields = ('title',)

class WishPhotoForm(forms.ModelForm):
  class Meta:
    model = WishPhoto
    fields = ('photo', )
