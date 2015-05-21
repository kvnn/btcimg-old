from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from btcimg.libs.common.forms.fields import BCAddressField
from .models import Asset


class AssetForm(ModelForm):
    btc_address = BCAddressField(label=_("Bitcoin Address"),
                                 help_text=_("Please use an address with no previous transactions."))

    class Meta:
        model = Asset
        fields = ['name', 'btc_address', 'private_image']
        labels = {
            'private_image': 'Image'
        }
