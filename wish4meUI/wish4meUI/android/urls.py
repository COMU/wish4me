#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    url(r'^flogin$', view='wish4meUI.android.views.facebook_login', name='Facebook_login'),
    url(r'^newidea$', view='wish4meUI.android.views.newIdea', name='new_idea'),
    url(r'^listmywishes$', view='wish4meUI.android.views.listMyWishes', name='my_wishes')
    )