from django import forms
from django.forms import modelformset_factory
from django import forms
from .models import BillItem

class CreateBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('description','quantity','price_per_quantity','total'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             )
        widgets={'description': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Description'}),
        'quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Quantity'}),
        'price_per_quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Price Per Quantity'}),
        'total': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Total'}),
        
        }