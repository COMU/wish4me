#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    url(r'^$', view='wish4meUI.main.views.home', name='homePage'),
    url(r'^welcome^$', view='wish4meUI.main.views.welcome', name='welcome_page'),
    url(r'^list_friends_wishes$', view='wish4meUI.main.views.list_friends_wishes', name='list_friends_wishes'),
    # (r'^wish4meUI/', include('wish4meUI.foo.urls')),
    (r'^foursq/', include('wish4meUI.foursq.urls')),
    (r'^twitter/', include('wish4meUI.twitter_app.urls')),
    (r'^facebook/', include('wish4meUI.facebook.urls')),
    (r'^google/', include('wish4meUI.google.urls')),
    (r'^wish/', include('wish4meUI.wish.urls')),
    (r'^user/', include('wish4meUI.userprofile.urls')),
    (r'^friend/', include('wish4meUI.friend.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #(r'^home$', 'wish4meUI.wish.views.home'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
