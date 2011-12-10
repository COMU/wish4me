from django.conf.urls.defaults import patterns, include, url
from facebook.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^login/$', 'django_openid_auth.views.login_begin',
        name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete',
        name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout'),
)
