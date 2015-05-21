from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('btcimg.apps.api.urls', namespace='api')),
    url(r'^', include('btcimg.apps.locker.urls', namespace='locker')),
    url(r'^', include('btcimg.apps.communications.urls', namespace='communications')),
)

if settings.DEBUG:
# for static assets during development
    urlpatterns += staticfiles_urlpatterns()
    # for media assets during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
