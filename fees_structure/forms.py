from .models import BillingItem
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms


class BillingItemModelForm(BSModalModelForm):
    class Meta:
        model = BillingItem
        fields = [
            'item',
            'charge_on_registration',
            'grades',
            'amount',
            'ocurrence',
            'terms',
            'year',
            'term',
        ]
        widgets = {
            'ocurrence': forms.RadioSelect()
        }
