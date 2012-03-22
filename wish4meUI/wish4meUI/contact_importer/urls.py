from django.conf.urls.defaults import *
from contact_importer.views import *

urlpatterns = patterns('',
    url(r'^$', view=home),
)
