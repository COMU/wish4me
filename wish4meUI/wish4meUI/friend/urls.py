from django.conf.urls.defaults import *

urlpatterns = patterns('friend.views',
    url(r'^follow/(?P<following_user_id>\d+)$',  view='follow',      name='friend_follow'),
    url(r'^follow_multiple$',  view='follow_multiple_users',      name='friend_follow_multiple'),
    url(r'^list_friends$',  view='listFriends',      name='friend_all_list'),
    url(r'^follow_back/(?P<invite_id>\d+)$',  view='acceptInvite',      name='friend_accept'),
)
