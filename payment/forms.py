from .models import Payment

from bootstrap_modal_forms.forms import BSModalModelForm


class PaymentModelForm(BSModalModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'student', 'invoice']

    def __init__(self, *args, **kwargs):
        self.invoice = kwargs.pop('invoice')
        self.student = kwargs.pop('student')
        super(PaymentModelForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].initial = self.invoice
        self.fields['student'].initial = self.student
        self.fields['student'].widget.attrs['readonly'] = True
        self.fields['invoice'].widget.attrs['readonly'] = True

    # You have to validate that the amount is greatter than 1
    def clean(self):
        super(PaymentModelForm,self).clean()
        #the aomunt should not be greateer than the invoice's balance
        amount = self.cleaned_data.get('amount')
        invoice = self.cleaned_data.get('invoice')

        if int(amount) > invoice.balance:
            self._errors['amount'] = self.error_class(['Cannot pay amount greater than invoice balance'])
        
        return self.cleaned_data