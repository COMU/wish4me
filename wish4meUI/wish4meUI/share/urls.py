from django.conf.urls.defaults import *
from share.views import *

urlpatterns = patterns('',
    url(r'^$', view=home),
    url(r'^facebook$', view=facebook),
    url(r'^twitter$', view=twitter),
)
