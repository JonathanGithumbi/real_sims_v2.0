from unicodedata import decimal
from django.db import models
from django import utils

from vendor.models import Vendor
from quickbooks.objects import Bill as qb_bill
from quickbooks.objects.base import Ref

class Bill(models.Model):
    bill_number = models.CharField(max_length=30, null=True,default=None,unique=True)
    created = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=7,decimal_places=2,null=True, default=None)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.bill_number 

class BillItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING,null=True, default=None)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7,decimal_places=2)
    price_per_quantity = models.DecimalField(max_digits=7,decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    synced = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    bill_number = models.CharField(max_length=255)
    qb_bill_id = models.CharField(max_length=255,null=True, default=None)
    
    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #create bill item
        bill = qb_bill()
        #create a vendor ref obj
        vendor_ref = Ref()
        vendor_id = self.vendor.qb_vendor_id
        vendor_ref.value = vendor_id
        
        bill.VendorRef = vendor_ref
        #bill.Line = 
        #bill.CurrencyRef=



