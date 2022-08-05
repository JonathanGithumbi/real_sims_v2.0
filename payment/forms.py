from django import forms 
from django.forms import modelformset_factory,Select
from django import forms
from .models import Payment

class CreatePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['qb_id','synced','student']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        widgets={ 
        'amount': forms.NumberInput(attrs={'class':'form-control', 'id':'quantity','value':0}),
        'date_paid': forms.DateInput(attrs={'class':'form-control', 'id':'floatingInput'}),
        }