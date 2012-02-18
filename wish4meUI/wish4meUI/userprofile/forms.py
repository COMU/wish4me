#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


def check_username(value):
    try:
        User.objects.get(username=value)
        return False
    except User.DoesNotExist:
        print "hede"
        pass

class UserSearchForm(forms.Form):
  term = forms.CharField(label='Search term', required=True, widget=forms.TextInput(attrs={'size': '60',}))

class UserInformationForm(forms.ModelForm):
    photo = forms.IntegerField()
    password = forms.CharField(
        help_text='', required=False
    )
    username = forms.CharField(
        required=False,
        validators=[check_username]
    )
    class Meta:
        fields = ('photo', 'username', 'first_name', 'last_name', 'email', 'password')
        model = User

