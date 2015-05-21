from rest_framework import serializers

from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ('id', 'name', 'unlock_value', 'btc_address', 'url', 'public_image',)

    def get_url(self, obj):
        return obj.get_absolute_url()
