from django import forms 
from django.forms import modelformset_factory,Select
from django import forms
from .models import Payment
from dal import autocomplete

class PaymentCreationForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['qb_id','synced','invoice','note']
        widgets={
        'student':autocomplete.ModelSelect2(url='student-autocomplete',attrs={'class':'form-select form-control form-control-sm','id':'student'}),
        'date_paid': forms.DateInput(attrs={'class':'form-control form-control-sm', 'id':'floatingInput','type':'date'}),
        'amount': forms.NumberInput(attrs={'class':'form-control form-control-sm', 'id':'quantity','min':1}),
        }

    #You have to validate that the amount is greatter than 1