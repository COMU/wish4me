#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    url(r'^flogin$', view='wish4meUI.android.views.facebook_login', name='android_facebook_login'),
    url(r'^listmywishes$', view='wish4meUI.android.views.listMyWishes', name='android_my_wishes'),
    url(r'^listfollowingwishes$', view='wish4meUI.android.views.listFollowingWishes', name='anroid_following_wishes'),
    url(r'^addnewwish$', view='wish4meUI.android.views.add_new_wish', name='anroid_add_new_wish')
    )