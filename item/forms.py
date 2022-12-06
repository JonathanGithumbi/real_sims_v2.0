from django.forms import ModelForm
from .models import Item
from django import forms


class CreateSalesItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'})
        }


class EditSalesItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'})
        }
