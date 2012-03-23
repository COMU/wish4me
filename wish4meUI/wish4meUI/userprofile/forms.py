#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django import forms

GENDER=(
        ('M', 'Male'),
        ('F', 'Female'),
)

class UserSearchForm(forms.Form):
  search_query = forms.CharField(label='search_query', required=True, widget=forms.TextInput(attrs={'size': '60',}))

class UserInformationForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=GENDER)
    password = forms.CharField(
        help_text='', required=False
    )
    username = forms.CharField(
        required=False
    )
    is_private = forms.BooleanField(required=False)
    class Meta:
        fields = ('photo', 'username', 'first_name', 'last_name', 'gender', 'email', 'password')
        model = User

