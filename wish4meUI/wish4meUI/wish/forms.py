from django import forms
from django.contrib.auth.models import User

from ajax_select import make_ajax_field

from wish4meUI.wish.models import Wish, WishCategory, Wishlist, WishPhoto
from wish4meUI.friend.models import Following

class WishForm(forms.ModelForm):

  def __init__(self, requested_user, *args, **kwargs):
    super(WishForm, self).__init__(*args, **kwargs)

    wishlists = Wishlist.objects.filter(owner = requested_user, is_hidden = False)
    self.fields["related_list"].queryset = wishlists
  #End of __init__

  wish_for_widget = forms.TextInput(attrs={'data-items': 4, 'data-provide': 'typeahead', 'autocomplete': 'off'})
  
  wish_for_text = forms.CharField(widget=wish_for_widget)


  class Meta:
    model = Wish
    fields = ('wish_for_text', 'description', 'category', 'related_list', 'brand', 'name', 'is_private' )
    
    #exclude = ('request_date', 'accomplish_date', 'is_hidden', 'wish_for')

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
