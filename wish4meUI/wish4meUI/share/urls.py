from django.conf.urls.defaults import *
from share.views import *

urlpatterns = patterns('',
    url(r'^$', view=home),
    url(r'^show/(?P<wish_id>\d+)$', view=show, name="wish_show_wish_alone"),
)
