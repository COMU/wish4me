from django import forms
from django.contrib.auth.models import User

from ajax_select import make_ajax_field

from wish4meUI.wish.models import Wish, WishCategory, WishPhoto, WishAccomplish, WishLocation
from wish4meUI.wishlist.models import Wishlist
from wish4meUI.friend.models import Following

class WishForm(forms.ModelForm):

  def __init__(self, requested_user, *args, **kwargs):
    super(WishForm, self).__init__(*args, **kwargs)

    wishlists = Wishlist.objects.filter(owner = requested_user, is_hidden = False)
    self.fields["related_list"].queryset = wishlists
    self.fields["wish_for_text"].label = "Wish for"
    if not self.fields["wish_for_text"].initial:
      self.fields["wish_for_text"].initial = requested_user.username
    #self.fields['location'].widget.attrs['id'] = "location"
    #self.fields['location'].required = False

  #End of __init__

  wish_for_widget = forms.TextInput(attrs={'data-items': 4, 'data-provide': 'typeahead', 'autocomplete': 'off'})
  wish_for_text = forms.CharField(widget=wish_for_widget)

  #location_widget = forms.TextInput(attrs={'data-items': 4, 'data-provide': 'typeahead', 'autocomplete': 'off', 'id':'location'})
  #location = forms.CharField(widget=location_widget)
  #location_widget = forms.Select(attrs={'id':'location'})
  #location = forms.ChoiceField(widget=location_widget)

  def clean(self):
    cleaned_data = self.cleaned_data
    print "cleaned data:", cleaned_data

    wish_for_text = cleaned_data.get('wish_for_text')
    related_list= cleaned_data.get('related_list')

    #since we do not know who the user is, we check the Wishlist owner to get user.
    #user_id = Wishlist.objects.get(pk = related_list).values('owner')
    user_id = related_list.owner.id
    followers = Following.objects.filter(to_user = user_id).values('id')
    followed = Following.objects.filter(from_user = user_id).values('id')

    related_people = followers | followed
    related_people = User.objects.filter(id__in = related_people)
    print "owner = ", related_list.owner.username, type(related_list.owner.username)
    print "wish for = ", wish_for_text, type(wish_for_text)
    if related_list.owner.username != wish_for_text:
      print "not equal"
    if related_list.owner.username != wish_for_text:
      if related_people.filter(username = wish_for_text).count() < 1:
        msg = u"Username does not match related people"
        self._errors['wish_for_text'] = self.error_class([msg])
        #since this field is not valid
        del cleaned_data['wish_for_text']
        raise forms.ValidationError("Username does not match related people")
    return cleaned_data

  class Meta:
    model = Wish
    fields = ('wish_for_text', 'description', 'category', 'related_list', 'brand', 'name', 'is_private' )

    #exclude = ('request_date', 'accomplish_date', 'is_hidden', 'wish_for')

  #wish_for  = make_ajax_field(User, 'username', 'user-channel', help_text='', label='Wish For')

class WishCategoryForm(forms.ModelForm):
  class Meta:
    model = WishCategory

class WishPhotoForm(forms.ModelForm):
  class Meta:
    model = WishPhoto
    fields = ('photo', )

  url = forms.CharField(max_length=200, required=False)

class AccomplishForm(forms.ModelForm):
  
  class Meta:
    model = WishAccomplish
    fields = ( 'comment',)

class WishLocationForm(forms.ModelForm):
  location_id = forms.IntegerField(widget=forms.HiddenInput())
  class Meta:
    model = WishLocation
    fields = ('name', 'address', 'city', 'state', 'country')
