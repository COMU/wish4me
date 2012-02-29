from django import forms
from wish4meUI.wish.models import Wish, WishCategory, Wishlist, WishPhoto

class WishForm(forms.ModelForm):
  class Meta:
    model = Wish
    exclude = ('request_date', 'accomplish_date', 'is_hidden', )

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
