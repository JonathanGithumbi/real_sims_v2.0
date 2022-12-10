from .models import Vendor

from bootstrap_modal_forms.forms import BSModalModelForm


class VendorModelForm(BSModalModelForm):
    class Meta:
        model = Vendor
        fields = ['name','phone_number']
