from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wishlist.views import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^home$', view=myWishlists, name='home-wishlist')
  url(r'^add$', view=add, name='add-wishlist')
  url(r'^(?P<wishlist_id>\d+)/show$', show, name='show-wishlist'),
  url(r'^(?P<wishlist_id>\d+)/edit$', edit, name='edit-wishlist'),
  url(r'^(?P<wishlist_id>\d+)/remove$', delete, name='remove-wishlist'),
)

