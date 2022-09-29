from django import forms 
from django.forms import modelformset_factory,Select
from django import forms
from .models import Payment

class PaymentCreationForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['qb_id','synced','invoice','note']
        widgets={
        'student':Select(attrs={'class':'form-select form-control form-control-sm','id':'student'}),
        'date_paid': forms.DateInput(attrs={'class':'form-control form-control-sm', 'id':'floatingInput','type':'date'}),
        'amount': forms.NumberInput(attrs={'class':'form-control form-control-sm', 'id':'quantity','value':0,'min':1}),
        }

    #You have to validate that the amount is greatter than 1