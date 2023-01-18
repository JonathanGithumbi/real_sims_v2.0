from .models import Bill
from .models import BillItem, BillPayment, CashTransaction
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
        widgets = {
            'total': forms.NumberInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        self.bill_obj = kwargs.pop('bill_obj', None)
        super(BillItemModelForm, self).__init__(*args, **kwargs)
        self.fields['bill'].initial = self.bill_obj


class BillPaymentModelForm(BSModalModelForm):
    class Meta:
        model = BillPayment
        fields = ['billitem', 'payment_date', 'amount']

    def __init__(self, *args, **kwargs):
        self.billitem = kwargs.pop('billitem')
        super(BillPaymentModelForm, self).__init__(*args, **kwargs)
        self.fields['billitem'].initial = self.billitem


class TopUpForm(forms.Form):
    amount = forms.IntegerField(
        widget=forms.NumberInput
        (attrs={'class': 'form-control form-control-sm', 'id': 'amount'}))


class CashTransactionModelForm(BSModalModelForm):
    class Meta:
        model = CashTransaction
        fields = ['operation', 'amount', 'date']

    def __init__(self, *args, **kwargs):
        super(CashTransactionModelForm, self).__init__(*args, **kwargs)
        self.fields['operation'].initial = 'Deposit'
