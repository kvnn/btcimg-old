from django.contrib import admin

from btcimg.apps.locker.models import Asset


class AssetAdmin(admin.ModelAdmin):
    fields = ('name', 'unlock_value', 'btc_address', 'public_image_blur_ratio',
              'public_image', 'private_image', 'blocked')

admin.site.register(Asset, AssetAdmin)
