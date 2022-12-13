from .models import Bill
from .models import BillItem
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm


class BillModelForm(BSModalModelForm):
    class Meta:
        model = Bill
        fields = ['vendor', 'billing_date']


class BillItemModelForm(BSModalModelForm):
    class Meta:
        model = BillItem
        fields = ['description', 'quantity',
                  'price_per_quantity', 'total', 'bill']


class TopUpForm(forms.Form):
    amount = forms.IntegerField(
        widget=forms.NumberInput
        (attrs={'class': 'form-control form-control-sm', 'id': 'amount'}))
