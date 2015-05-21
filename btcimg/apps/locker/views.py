import requests
from decimal import Decimal

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Asset
from .forms import AssetForm


def _satoshi_to_bitcoin(num_satoshi):
    return Decimal(0.00000001 * num_satoshi)


class AssetView(generic.View):
    def _get_btc_received(self, asset):
        '''Returns a Decimal value or None'''
        url = 'https://blockchain.info/address/%s?format=json&limit=0' % asset.btc_address
        req = requests.get(url)
        if req.status_code == 200:
            if 'total_received' in req.json():
                return _satoshi_to_bitcoin(req.json()['total_received'])
        return 0

    def get(self, request, *args, **kwargs):
        asset = get_object_or_404(Asset, slug=kwargs['slug'])
        btc_received = self._get_btc_received(asset)

        btc_left = asset.unlock_value - btc_received

        data = {
            'asset': asset,
            'btc_left': btc_left,
            'public_image': asset.get_public_image(btc_received),
            'btc_received': btc_received,
        }
        return render(request, 'locker/detail.html', data)


class AssetCreate(generic.edit.CreateView):
    model = Asset
    form_class = AssetForm

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.fields['owner'] = self.request.user.id
        return super(AssetCreate, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class AssetList(generic.TemplateView):
    template_name = 'locker/list.html'
