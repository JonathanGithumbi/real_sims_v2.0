from django.shortcuts import render
from requests import request
from .models import Invoice,Item

def invoice_detail(request,id,s):
    invoice = Invoice.objects.get(id=id)
    items =  Item.objects.filter(invoice=invoice)
    return render (request,'invoice/invoice_detail.html',{'invoice':invoice,'items':items})


