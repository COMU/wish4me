from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wish4meUI/', include('wish4meUI.foo.urls')),
    (r'^foursq_auth/', include('wish4meUI.foursq_auth.urls')),
    (r'^twitter/', include('wish4meUI.twitter_app.urls')),
    (r'^facebook/', include('wish4meUI.facebook.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
