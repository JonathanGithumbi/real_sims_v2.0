from django import forms 
from django.forms import modelformset_factory,Select
from django import forms
from .models import BillItem

class CreateBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('vendor','description','quantity','price_per_quantity','total')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        widgets={
        'vendor':Select(attrs={'class':'form-select form-control form-control-sm','id':'vendor'}),
        'description': forms.TextInput(attrs={'class':'form-control form-control-sm', 'id':'floatingInput','placeholder':'Description'}),
        'quantity': forms.NumberInput(attrs={'class':'form-control form-control-sm', 'id':'quantity','value':0}),
        'price_per_quantity': forms.NumberInput(attrs={'class':'form-control form-control-sm', 'id':'price_per_quantity','value':0}),
        'total': forms.NumberInput(attrs={'class':'form-control form-control-sm', 'id':'total','value':0}),
        
        }


class EditBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('vendor', 'description', 'quantity', 'price_per_quantity', 'total')
        widgets = {
            'vendor': Select(attrs={'class': 'form-select form-control form-control-sm','id':'vendor'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'placeholder': 'Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'quantity', 'value': 0}),
            'price_per_quantity': forms.NumberInput(
                attrs={'class': 'form-control form-control-sm', 'id': 'price_per_quantity', 'value': 0}),
            'total': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'total', 'value': 0}),

        }