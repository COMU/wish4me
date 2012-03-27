from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wishlist.views import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^home$', view=myWishlists, name='wishlist-home'),
  url(r'^add$', view=add, name='wishlist-add'),
  url(r'^(?P<wishlist_id>\d+)/show$', show, name='wishlist-show'),
  url(r'^(?P<wishlist_id>\d+)/rename$', rename, name='wishlist-rename'),
  url(r'^(?P<wishlist_id>\d+)/remove$', remove, name='wishlist-remove'),
  url(r'^(?P<wishlist_id>\d+)/setPrivacy$', setPrivacy, name='wishlist-setPrivacy'),
)

