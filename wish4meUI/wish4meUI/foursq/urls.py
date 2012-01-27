from django.conf.urls.defaults import *
from foursq.views import *

urlpatterns = patterns('foursq.views',
    # main page redirects to start or login
    url(r'^$', view=main, name='main_view'),
    # receive OAuth token from 4sq
    url(r'^callback/$', view='callback', name='oauth_return'),
    # logout from the app
    url(r'^logout/$', view='unauth', name='oauth_unauth'),
    # authenticate with 4sq using OAuth
    url(r'^auth/$', view='auth', name='foursq_oauth_auth'),
    # main page once logged in
    url( r'^done/$', view='done', name='foursq_oauth_done' ),
    # friend import page
    url( r'^friend_import/$', view='friend_import', name='friend_import' ),
)
