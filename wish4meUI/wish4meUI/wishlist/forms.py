from django import forms
from django.contrib.auth.models import User

from wish4meUI.wishlist.models import Wishlist

class WishlistForm(forms.ModelForm):
  class Meta:
    model = Wishlist
    fields = ('title', )
