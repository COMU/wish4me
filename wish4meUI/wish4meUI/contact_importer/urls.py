from django.conf.urls.defaults import *
from contact_importer.views import *

urlpatterns = patterns('',
    url(r'^(?P<importing_profile>\w+)$', view=contact_importer_home, name="contact_importer_home"),
)
