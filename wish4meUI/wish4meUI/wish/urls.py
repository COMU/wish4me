from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wish.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
#    url(r'^add_wish$', view=addWish, name="addWish"),
    url(r'^list_wish-(?P<wish_category_id>\d+)/$', view=listWish),
#    url(r'^add_wish_category$', view=addWishCategory, name="addWishCategory"),
    url(r'^list_wish_category$', view=listWishCategory),

#    url(r'^login$', view=login),
#    url(r'^newsfeed$', view=newsfeed),
#    url(r'^authentication_callback$', view=authentication_callback),
#    url(r'^logout$', view='django.contrib.auth.views.logout'),

)
