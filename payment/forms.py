from .models import Payment

from bootstrap_modal_forms.forms import BSModalModelForm


class PaymentModelForm(BSModalModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

    # You have to validate that the amount is greatter than 1
