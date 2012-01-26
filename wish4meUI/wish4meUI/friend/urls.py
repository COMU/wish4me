from django.conf.urls.defaults import *

urlpatterns = patterns('friend.views',
    url(r'^follow/(?P<following_user_id>\d+)$',  view='follow',      name='friend_follow'),
    url(r'^list_followers$',  view='listFollowers',      name='friend_followers'),
    url(r'^follow_back/(?P<invite_id>\d+)$',  view='acceptInvite',      name='friend_accept'),
)
