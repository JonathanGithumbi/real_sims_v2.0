from django import forms
from django import forms
from .models import Expense
from django.forms import Select


class CreateExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
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


class EditExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
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
