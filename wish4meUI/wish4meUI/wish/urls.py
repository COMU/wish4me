from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wish.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', view=homeWish, name="home"),
#    url(r'^add_wish$', view=addWish, name="addWish"),
    #url(r'^list_wish-(?P<wish_category_id>\d+)/$', view=listWish),
    url(r'^list_wish-(?P<wishlist_id>\d+)/$', view=listWish, name='list_wish'),
#    url(r'^add_wish_category$', view=addWishCategory, name="addWishCategory"),
    url(r'^list_wish_category$', view=listWishCategory),

    url(r'^list_wishlist$', view=listWishlist),
    url(r'^add_wishlist$', view=addWishlist, name="addWishlist")


)
