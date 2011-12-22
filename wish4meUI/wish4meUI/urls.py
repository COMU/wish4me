from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wish4meUI/', include('wish4meUI.foo.urls')),
    (r'^foursq_auth/', include('wish4meUI.foursq.urls')),
    (r'^twitter/', include('wish4meUI.twitter_app.urls')),
    (r'^facebook/', include('wish4meUI.facebook.urls')),
    (r'^google/', include('wish4meUI.google.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^home$', 'wish4meUI.wish.views.home'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
