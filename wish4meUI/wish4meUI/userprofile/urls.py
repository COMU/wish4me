from django.conf.urls.defaults import *

urlpatterns = patterns('userprofile.views',
    url(r'^logout/$',       view='userLogout',            name='user_logout'),
    url(r'^profile/$',      view='userProfile',           name='user_profile'),
    url(r'^List_all$',      view='userListAll',           name='user_list_all'),
    url(r'^loginSuccess$',  view='userLoginSuccess',      name='user_loginSuccess'),
    url(r'^loginFail$',     view='userLoginFail',         name='user_loginFail'),
)
