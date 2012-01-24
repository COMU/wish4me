from django import forms
from wish4meUI.wish.models import Wish, WishCategory, Wishlist

class WishForm(forms.ModelForm):
  class Meta:
    model = Wish
    fields = ('wish_for', 'comment', 'category', )

class WishCategoryForm(forms.ModelForm):
  class Meta:
    model = WishCategory

class WishlistForm(forms.ModelForm):
  class Meta:
    model = Wishlist
    fields = ('comment',)

