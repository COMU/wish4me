from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wish.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', view=homeWish, name="wish_home"),
    url(r'^wish/add/(?P<wishlist_id>\d+)$', view=addWish, name="wish_add_wish"),
    #url(r'^list_wish-(?P<wish_category_id>\d+)/$', view=listWish),
    url(r'^wish/list/(?P<wishlist_id>\d+)$', view=listWish, name='wish_list_wish'),
#    url(r'^add_wish_category$', view=addWishCategory, name="addWishCategory"),
    url(r'^wishcategory/list$', view=listWishCategory, name="wish_list_wishcategory"),

    url(r'^wishlist/list$', view=listWishlist, name="wish_list_wishlist"),
    url(r'^wish/list/all$', view=listAllWishes, name="wish_list_allwishes"),
    url(r'^wishlist/add$', view=addWishlist, name="wish_add_wishlist")


)
