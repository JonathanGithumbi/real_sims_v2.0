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
        return self.vendor.name + ": " + str(self.billing_date)

    def get_total_amount(self):
        amount = 0
        for item in self.billitem_set.all():
            amount = amount + item.total

        return amount

    def get_amount_due(self):

        if self.billitem_set.all().count() > 0:
            amount_due = 0
            for item in self.billitem_set.all():
                amount_due += item.amount_due
            return amount_due
        else:
            return 0

    def payment_status(self):
        if self.get_total_amount() == 0:
            return 'empty'
        if self.get_amount_due() == 0:
            return 'paid'
        if self.get_total_amount() == self.get_amount_due():
            return 'unpaid'

        if self.get_amount_due() < self.get_total_amount():
            return 'partially-paid'


class BillItem(models.Model):
    """This is a table for petty cash bill items"""
    """every row in this table is a transaction that affects the petty cash balance ; the transaction may increase the balance such as a deposit or could decrease the balance such as a bill item"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_per_quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    # varies every time a payment is made
    # should be set to == total on pre_save
    # the amount that changes when a payment is created, updated and deleted
    amount_due = models.IntegerField(null=True)

    def __str__(self):
        return self.description

    def get_petty_cash_balance(self):
        return self.petty_cash_balance

    def get_amount_due(self):
        if self.billpayment_set.all().count() > 0:
            amount_paid = 0
            for payment in self.billpayment_set.all():
                amount_paid += payment.amount

            amount_due = self.total - amount_paid
            return amount_due
        else:
            return self.total

    def get_total_amount(self):
        return self.total

    def payment_status(self):
        if self.get_total_amount() == 0:
            return 'empty'
        if self.get_amount_due() == 0:
            return 'paid'
        if self.get_amount_due() == self.total:
            return 'unpaid'
        if self.get_amount_due() < self.total:
            return 'partially-paid'


class BillPayment(models.Model):
    billitem = models.ForeignKey(BillItem, on_delete=models.CASCADE)
    creation_day = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    payment_date = models.DateField()

# obsolete remove when able


class Cash(models.Model):
    OPERATION_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw')
    ]
    operation = models.CharField(max_length=255, choices=OPERATION_CHOICES)
    amount = models.IntegerField()
    day = models.DateField()


class CashTransaction(models.Model):
    OPERATION_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw')
    ]
    operation = models.CharField(max_length=255, choices=OPERATION_CHOICES)
    amount = models.IntegerField()
    date = models.DateField()
    payment = models.ForeignKey(
        BillPayment, on_delete=models.CASCADE, null=True)


class PettyCash(models.Model):
    """This Model Holds the balance of the petty cash account"""
    balance = models.IntegerField(default=0)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.balance
