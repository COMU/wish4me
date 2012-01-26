from django.conf.urls.defaults import *

urlpatterns = patterns('friend.views',
    url(r'^follow/(?P<following_user_id>\d+)$',  view='follow',      name='friend_follow'),
)
