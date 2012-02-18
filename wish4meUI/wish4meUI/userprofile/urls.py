from django.conf.urls.defaults import *

urlpatterns = patterns('userprofile.views',
    url(r'^logout/$',       view='userLogout',            name='user_logout'),
    url(r'^profile/$',      view='userProfile',           name='user_profile'),
    url(r'^profile/edit/$', view='userInformationEdit',   name='user_information_edit'),
    url(r'^List_all$',      view='userListAll',           name='user_list_all'),
    url(r'^search$',        view='userSearch',            name='user_search'),
    url(r'^loginSuccess$',  view='userLoginSuccess',      name='user_loginSuccess'),
    url(r'^loginFail$',     view='userLoginFail',         name='user_loginFail'),
)
