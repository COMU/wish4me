from django import forms
from django.contrib.auth.models import User

from ajax_select import make_ajax_field

from wish4meUI.wish.models import Wish, WishCategory, WishPhoto

class WishForm(forms.ModelForm):
  class Meta:
    model = Wish
    exclude = ('request_date', 'accomplish_date', 'is_hidden', )

  wish_for  = make_ajax_field(User, 'username', 'user-channel', help_text='', label='Wish For')

class WishCategoryForm(forms.ModelForm):
  class Meta:
    model = WishCategory

class WishPhotoForm(forms.ModelForm):
  class Meta:
    model = WishPhoto
    fields = ('photo', )
