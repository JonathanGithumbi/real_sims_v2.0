from unicodedata import decimal
from django.db import models
from django import utils
class Bill(models.Model):
    bill_number = models.CharField(max_length=30, null=True,default=None,unique=True)
    created = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=7,decimal_places=2,null=True, default=None)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.bill_number 

class BillItem(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7,decimal_places=2)
    price_per_quantity = models.DecimalField(max_digits=7,decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    synced = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    bill_number = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

