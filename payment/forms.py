from django import forms
from django.forms import modelformset_factory, Select
from django import forms
from .models import Payment



class PaymentCreationForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student','date_paid','amount']
        widgets = {
            'student': Select(attrs={'class': 'form-select form-control form-control-sm payment-select', 'id': 'student'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'quantity', 'min': 1}),
        }

    # You have to validate that the amount is greatter than 1
