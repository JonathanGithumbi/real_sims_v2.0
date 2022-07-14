from django.shortcuts import render
from requests import request
from .models import Invoice,Item


def invoice_detail(request,id):
    invoice = Invoice.objects.get(id=id)
    items =  Item.objects.filter(invoice=invoice)
    amount = invoice.get_amount()
    return render (request,'invoice/invoice_detail.html',{'invoice':invoice,'items':items,'amount':amount})




