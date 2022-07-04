from django import forms
from django.shortcuts import render
from .models import Bill, BillItem
from django.forms import inlineformset_factory
from .utils import generate_bill_number
from django import forms


def bills(request):
    return render(request, 'bill/bills.html')


def create_bill(request):
    bill = Bill()
    BillItemInlineFormSet = inlineformset_factory(Bill, BillItem, fields=(
        'description', 'quantity', 'price_per_quantity', 'total'),
        widgets={
            'description': forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Description'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Quantity'}),
            'price_per_quantity': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Price Per Quantity'}),
            'total': forms.NumberInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Total'}),
        }, extra=2,)

    if request.method == 'GET':
        formset = BillItemInlineFormSet(instance=bill)
    if request.method == 'POST':
        pass
    
    return render(request,'bill/create_bill.html',{'formset':formset,'bill':bill})