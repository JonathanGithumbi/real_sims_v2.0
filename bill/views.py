from django import forms
from django.shortcuts import redirect, render
from .models import BillItem
from django.forms import modelformset_factory
from .utils import generate_bill_number
from django import forms
from .forms import CreateBillItemForm
from django.urls import reverse
from . import utils


def bills(request):
    bills = BillItem.objects.all()

    return render(request, 'bill/bills.html',{'bills':bills})


def create_bill(request):
    form = CreateBillItemForm()
    if request.method == 'GET':
        return render(request, 'bill/create_bill.html',{'form':form})
    if request.method == 'POST':
        form=CreateBillItemForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.bill_number = utils.generate_bill_number(instance.id)
            instance.save()
            return redirect(reverse('bills'))
        else:
            return render(request, 'bill/create_bill.html',{'form':form})



