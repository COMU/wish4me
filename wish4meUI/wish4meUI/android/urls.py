#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    url(r'^flogin$', view='wish4meUI.android.views.facebook_login', name='Facebook_login'),
    )