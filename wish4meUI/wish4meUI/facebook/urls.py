from django.conf.urls.defaults import patterns, include, url
from facebook.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', view=home),

    url(r'^login$', view=login, name='facebook_login'),
    url(r'^login_callback$', view=loginCallback, name='facebook_login_callback'),
    url(r'^newsfeed$', view=newsfeed),
    url(r'^logout$', view='django.contrib.auth.views.logout'),

)
