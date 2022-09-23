from django import forms
from django.shortcuts import redirect, render
from .models import BillItem
from django.forms import modelformset_factory
from .utils import generate_bill_number
from django import forms
from .forms import CreateBillItemForm
from django.urls import reverse
from . import utils
from bill_payment.models import BillPayment
from .forms import EditBillItemForm
from quickbooks import QuickBooks
from quickbooks.objects import Customer
from django.contrib import messages
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.objects import BillPayment as QB_BillPayment
from quickbooks.objects import BillPaymentLine
from quickbooks.objects import Vendor as qb_vendor
from quickbooks.objects import Bill as qb_bill
from quickbooks.objects.base import LinkedTxn
from quickbooks.objects import Account as QB_Account

from account.models import Account as Local_Account
from quickbooks.objects.billpayment import CheckPayment

def bills(request):
    bills = BillItem.objects.all().order_by('created')

    return render(request, 'bill/bills.html',{'bills':bills})


def create_bill(request):

    if request.method == 'GET':
        form = CreateBillItemForm()
        return render(request, 'bill/create_bill.html',{'form':form})
    if request.method == 'POST':
        form=CreateBillItemForm(request.POST)
        if form.is_valid():
            bill_item_obj = form.save()

            #also save the  bill to quickbooks
            try:
                qb_bill_item = bill_item_obj.create_qb_bill()
            except:
                pass
            else:
                bill_item_obj.qb_id = qb_bill_item.Id
                bill_item_obj.synced = True
                bill_item_obj.save(update_fields=['qb_id','synced'])
            messages.success(request,"{0} Bill recorded successfully".format(bill_item_obj.description),extra_tags='alert-success')
            return redirect(reverse('bills'))
        else:
            return render(request, 'bill/create_bill.html',{'form':form})

def pay_bill(request,id):
    bill_obj = BillItem.objects.get(pk=id)
    # create a bill payment object.
    # bill pay
    bill_payment_obj = BillPayment.objects.create(
        vendor=bill_obj.vendor,
        amount=bill_obj.total,
        bill=bill_obj,
    )
    bill_payment_obj.save()
    bill_obj.fully_paid = True
    bill_obj.save(update_fields=['fully_paid'])

    try:
        qb_bill_payment_obj = bill_payment_obj.create_qb_bill_payment_obj()
    except:
        pass
    else:
        bill_payment_obj.qb_id = qb_bill_payment_obj.Id
        bill_payment_obj.synced = True
        bill_payment_obj.save(update_fields=['qb_id', 'synced'])
    messages.success(request,"{0} Bill Payment recorded Successfully".format(bill_obj.description),extra_tags='alert-success')
    return redirect('bills')
def edit_bill(request,id):
    bill_obj = BillItem.objects.get(pk=id)

    if request.method=='GET':
        bill_edit_form = EditBillItemForm(instance=bill_obj)
        return render(request,'bill/edit_bill.html',{'form':bill_edit_form,'bill':bill_obj})
    if request.method == 'POST':
        initial_data = {
            'vendor':bill_obj.vendor,
            'description':bill_obj.description,
            'quantity':bill_obj.quantity,
            'price_per_quantity':bill_obj.price_per_quantity,
            'total':bill_obj.total
        }
        bill_edit_form = EditBillItemForm(request.POST,initial=initial_data)
        if bill_edit_form.is_valid():
            if bill_edit_form.has_changed():
                bill_obj.vendor = bill_edit_form.cleaned_data['vendor']
                bill_obj.description = bill_edit_form.cleaned_data['description']
                bill_obj.quantity = bill_edit_form.cleaned_data['quantity']
                bill_obj.price_per_quantity = bill_edit_form.cleaned_data['price_per_quantity']
                bill_obj.total = bill_edit_form.cleaned_data['total']
                bill_obj.save(update_fields=None)
                try:
                    qb_bill = bill_obj.edit_qb_bill()
                except:
                    pass
                messages.info(request,"{0} Bill Details changed successfully".format(bill_obj.description),extra_tags='alert-success')
                return redirect('bills')
            else:
                messages.info(request,"No Data Changed on {0} Bill".format(bill_obj.description),extra_tags='alert-info')
                return redirect('bills')
        else:
            bill_edit_form = EditBillItemForm(request.POST)
            return render(request,'bill/edit_bill.html',{'form':bill_edit_form})

