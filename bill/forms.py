from django import forms
from django.forms import modelformset_factory, Select
from django import forms
from .models import BillItem


class CreateBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('recipient', 'description', 'category',
                  'quantity', 'price_per_quantity', 'total')
        widgets = {
            'recipient': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipient'}),
            'description': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'description'}),
            'category': Select(attrs={'class': 'form-select form-control form-control-sm', 'id': 'category'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'quantity'}),
            'price_per_quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'price_per_quantity'}),
            'total': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'total'}),

        }


class EditBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('recipient', 'description', 'category', 'quantity',
                  'price_per_quantity', 'total')
        widgets = {
            'recipient': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipient'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'category': Select(attrs={'class': 'form-select form-control form-control-sm', 'id': 'category'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'quantity'}),
            'price_per_quantity': forms.NumberInput(
                attrs={'class': 'form-control form-control-sm', 'id': 'price_per_quantity'}),
            'total': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'total'}),

        }


class TopUpForm(forms.Form):
    amount = forms.IntegerField(
        widget=forms.NumberInput
        (attrs={'class': 'form-control form-control-sm', 'id': 'amount'}))
