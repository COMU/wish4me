from django.conf.urls.defaults import patterns, include, url
from wish4meUI.wish.views import *
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^home$', view=friendActivity, name='friend-activity'),
    url(r'^me$', myActivity, name='my-activity'),
    url(r'^(?P<friend_id>\d+)$', view=specificFriendActivity, name='specific-friend-activity'),


    url(r'^add$', add, name='add-wish'),
    url(r'^(?P<wish_id>\d+)/show$', show, name='show-wish'),
    url(r'^(?P<wish_id>\d+)/edit$', edit, name='edit-wish'),
    url(r'^(?P<wish_id>\d+)/change-status$', changeStatus, name='change-wish-status'),
    url(r'^wish/list/(?P<wishlist_id>\d+)$', view=list, name='wish-list'),
    #TODO(orc.avs) Remove below
    url(r'^wish/edit/(?P<wish_id>\d+)$', view=edit, name="wish_edit_wish"),
    url(r'^wish/show/(?P<wish_id>\d+)$', view=show, name="wish_show_wish_alone"),
    url(r'^accomplish/(?P<wish_id>\d+)$', view=accomplish, name="wish_accomplish_wish"),
    url(r'^remove/(?P<wish_id>\d+)$', view=remove, name="wish_remove_wish"),
    url(r'^respond/(?P<accomplish_id>\d+)/(?P<response>.*)$', view=respondAccomplish, name="wish_respond_accomplish"),
		url(r'^add_to_my_wishes/(?P<wish_id>\d+)$', view=add_to_my_wishes, name="wish_add_to_my_wishes"),
#url(r'^order/(?P<order>.*)/filter/(?P<filter_by>.*)/(?P<filter>.*)/(?P<page_number>\d+)/$', 'main',name='main_page'),
	#location based
	url(r'^locations$', view=getLocations, name='get-locations'),
	url(r'^add_location$', view=addLocation, name='new-location'),
	url(r'^search_location$', view=searchLocation, name='search-location'),

)

#TODO(orc.avs): Remove below
'''
urlpatterns = patterns('',
    url(r'^$', view=homeWish, name="wish_home"),
    url(r'^wish/add/$', view=addWish, name="wish_add_wish"),
    #url(r'^list_wish-(?P<wish_category_id>\d+)/$', view=listWish),
#    url(r'^add_wish_category$', view=addWishCategory, name="addWishCategory"),
    url(r'^wishcategory/list$', view=listWishCategory, name="wish_list_wishcategory"),
    url(r'^wishcategory/add$', view=addWishCategory, name="wish_add_wishcategory"),

    url(r'^wish/list/all$', view=listAllWishes, name="wish_list_allwishes"),
    (r'^comments/', include('django.contrib.comments.urls')),
)
'''
