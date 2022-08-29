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

from quickbooks import QuickBooks
from quickbooks.objects import Customer

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.objects import BillPayment as QB_BillPayment
from quickbooks.objects import BillPaymentLine
from quickbooks.objects import Vendor as qb_vendor
from quickbooks.objects import Bill as qb_bill


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

def pay_bill(request,id):
    BillItem.objects.filter(pk=id).update(status='paid')
    local_bill_obj = BillItem.objects.get(pk=id)
        #Reflect changes in the quickbooks by sparse updating the iinvoice
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    realm_id_obj = Token.objects.get(name='realm_id')
    #create an auth_client
    auth_client = AuthClient(
        client_id = settings.CLIENT_ID,
        client_secret = settings.CLIENT_SECRET,
        access_token = access_token_obj.key,
        environment=settings.ENVIRONMENT,
        redirect_uri = settings.REDIRECT_URI
    )
    #create a quickboooks client
    client = QuickBooks(
        auth_client = auth_client,
        refresh_token = refresh_token_obj.key,
        company_id = realm_id_obj.key
    )

    #create bill payment object
    local_bill_payment_obj = BillPayment.objects.create(
        bill = local_bill_obj,
        vendor = local_bill_obj.vendor
    )#qb_id,created, and synced to be updadted in .save() method

    local_bill_payment_obj.save()


    #get the qb_bill_item
    qb_bill_item = qb_bill.get(local_bill_obj.qb_id,qb=client)
    #construct bill payment line
    bill_paym_line = BillPaymentLine()
    bill_paym_line.Amount = local_bill_obj.total
    bill_paym_line.LinkedTxn.append(qb_bill_item)
    #get vendor bject 
    qb_vendor_obj = qb_vendor.get(local_bill_obj.vendor.qb_id, qb=client)
    #create qb bill payment object
    bill_paym_obj = QB_BillPayment()
    bill_paym_obj.vendor = qb_vendor_obj.to_ref()
    bill_paym_obj.TotalAmt = local_bill_obj.total
    bill_paym_obj.Line.append(bill_paym_line)
    bill_paym_obj.PayType = "Check"
    bill_paym_obj.save(qb=client)

    return redirect('bills')

