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
