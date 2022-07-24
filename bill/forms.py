from django import forms 
from django.forms import modelformset_factory,Select
from django import forms
from .models import BillItem

class CreateBillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ('vendor','description','quantity','price_per_quantity','total')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        widgets={
        'vendor':Select(attrs={'class':'form-select'}),    
        'description': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Description'}),
        'quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'quantity','value':0}),
        'price_per_quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'price_per_quantity','value':0}),
        'total': forms.NumberInput(attrs={'class':'form-control', 'id':'total','value':0}),
        
        }