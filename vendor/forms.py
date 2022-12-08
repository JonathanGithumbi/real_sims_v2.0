from django import forms
from django.forms import modelformset_factory
from django import forms
from .models import Vendor


class CreateVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'})

        }


class EditVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'})

        }
