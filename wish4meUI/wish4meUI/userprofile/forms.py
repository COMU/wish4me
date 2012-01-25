
from django import forms

class UserSearchForm(forms.Form):
  term = forms.CharField(label='Search term', required=True, widget=forms.TextInput(attrs={'size': '60',}))
