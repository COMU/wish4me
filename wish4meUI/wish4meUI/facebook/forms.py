from django import forms
from django.db import models

PUBLISH_CHOICES = (('1', 'Publish on Facebook News Feed'),('0', 'Do not publish on Facebook News Feed'),)

class NewsFeedForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea())
    facebook_pub = forms.ChoiceField(widget = forms.Select(), choices=PUBLISH_CHOICES, required = True,)

