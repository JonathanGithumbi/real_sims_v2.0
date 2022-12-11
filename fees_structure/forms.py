from .models import BillingItem
from bootstrap_modal_forms.forms import BSModalModelForm


class BillingItemModelForm(BSModalModelForm):
    class Meta:
        model = BillingItem
        fields = [
            'item',
            'charge_on_registration',
            'grades',
            'amount',
            'ocurrence',
            'period',
            'terms',
            'year',
            'term',
            ]
