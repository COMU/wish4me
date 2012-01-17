from django.conf.urls.defaults import patterns, include, url
from facebook.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', view=home),

    url(r'^login$', view=login),
    url(r'^newsfeed$', view=newsfeed),
    url(r'^authentication_callback$', view=authentication_callback),
    url(r'^logout$', view='django.contrib.auth.views.logout'),

)
