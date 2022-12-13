from django.db import models
from vendor.models import Vendor


class Bill(models.Model):
    PAYMENT_STATUS = [
        ('Fully Paid', 'Fully Paid'),
        ('Partly Paid', 'Partly Paid'),
        ('Unpaid', 'Unpaid')
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, null=True)
    billing_date = models.DateField(null=True)
    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.vendor.name


class BillItem(models.Model):
    """This is a table for petty cash bill items"""
    """every row in this table is a transaction that affects the petty cash balance ; the transaction may increase the balance such as a deposit or could decrease the balance such as a bill item"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_per_quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    def get_petty_cash_balance(self):
        return self.petty_cash_balance


class PettyCash(models.Model):
    balance = models.IntegerField(default=0)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.balance
