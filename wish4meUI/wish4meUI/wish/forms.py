from django import forms
from wish4meUI.wish.models import Wish, WishCategory, WishList

class WishForm(forms.ModelForm):
    class Meta:
        model = Wish

class WishCategoryForm(forms.ModelForm):
    class Meta:
        model = WishCategory

class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList

