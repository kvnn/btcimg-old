from django.conf.urls import patterns, url

from .views import AssetView, AssetCreate, AssetList

urlpatterns = patterns('',
    url(r'^create/', AssetCreate.as_view(), name='asset-create'),
    url(r'^list/', AssetList.as_view(), name='asset-list'),
    url(r'^img/(?P<slug>[\w\-\.\~\+&,]+)/', AssetView.as_view(), name='asset-detail'),
)
