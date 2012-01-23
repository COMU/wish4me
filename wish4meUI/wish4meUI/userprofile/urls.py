from django.conf.urls.defaults import *

from twitter_app.views import *

urlpatterns = patterns('userprofile.views',
    url(r'^logout/$',  view='userLogout',      name='user_logout'),
    url(r'^profile/$', view='userProfile',     name='user_profile'),
    url(r'^loginSuccess$', view='userLoginSuccess',     name='user_loginSuccess'),
)
