from django.conf.urls import patterns, url

from rest_framework import generics, permissions, filters

from .serializers import AssetSerializer
from .models import Asset


class AssetList(generics.ListAPIView):
    queryset = Asset.objects.filter(blocked=False)
    serializer_class = AssetSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created')
    ordering = ('-created',)
    paginate_by = 20

    # @cache_response(60 * 60)
    def get(self, request, *args, **kwargs):
        return super(AssetList, self).get(request, *args, **kwargs)

urlpatterns = patterns('',
    url(r'^$', AssetList.as_view(), name='list'),
)
