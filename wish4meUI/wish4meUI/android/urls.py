#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    url(r'^flogin$', view='wish4meUI.android.views.facebook_login', name='android_facebook_login'),
    url(r'^newidea$', view='wish4meUI.android.views.newIdea', name='android_new_idea'),
    url(r'^listmywishes$', view='wish4meUI.android.views.listMyWishes', name='android_my_wishes'),
    url(r'^listfollowingwishes$', view='wish4meUI.android.views.listFollowingWishes', name='anroid_following_wishes')
    )