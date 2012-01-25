from django.conf.urls.defaults import *

urlpatterns = patterns('friend.views',
    url(r'^invite/(?P<friend_id>\d+)$',  view='invite',      name='friend_invite'),
)
