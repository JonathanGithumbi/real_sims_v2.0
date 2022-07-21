from django import forms
from django.forms import modelformset_factory
from django import forms
from .models import Vendor

class CreateVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('given_name','middle_name','last_name')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        widgets={

        'given_name': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'First name'}),
        'middle_name': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Middle Name'}),
        'last_name': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Last Name'}),
        
        }