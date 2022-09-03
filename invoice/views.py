from django.shortcuts import render
from requests import request

from payment.models import Payment
from .models import Invoice,Item #Item refers to invoice_item


def invoice_detail(request,id):
    invoice = Invoice.objects.get(id=id)
    items = Item.objects.filter(invoice=invoice)
    payments = Payment.objects.filter(invoice=invoice)

    return render (request,'invoice/invoice_details.html',{'invoice':invoice,'items':items,'payments':payments})




