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
    def clean(self):
        super(BillItemModelForm,self).clean()

        quantity = self.cleaned_data.get('quantity')
        ppq = self.cleaned_data.get('price_per_quantity')

        if quantity < 0 : 
            self._errors['quantity'] = self.error_class(['Enter a valid quantity'])
        if ppq < 0 : 
            self._errors['price_per_quantity'] = self.error_class(['Enter a valid price'])

        return self.cleaned_data


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

    def clean(self):
        super(BillPaymentModelForm,self).clean()
        billitem = self.cleaned_data.get('billitem')
        amount = self.cleaned_data.get('amount')

        if amount > billitem.amount_due:
            self._errors['amount'] = self.error_class(['Cannot pay amount greater than bill balance'])

        if amount <= 0: 
            self._errors['amount'] = self.error_class(['Enter a valid amount']) 

        return self.cleaned_data

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
        
    def clean(self):
        super(CashTransactionModelForm,self).clean()

        amount = self.cleaned_data.get('amount')

        if amount <= 0 :
            self._errors['amount'] = self.error_class(['Please enter a valid amount'])

        return self.cleaned_data
