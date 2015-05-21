from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns(
    '',
    url(r'^v1.0/img/', include('btcimg.apps.locker.api', namespace='core')),
)
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'jsonp', 'api'])
