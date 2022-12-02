from django.db import models
from student.models import Student
from invoice.models import Invoice
from quickbooks import QuickBooks
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Payment as QB_Payment
from quickbooks.objects import PaymentLine
from quickbooks.objects import Customer
from quickbooks.objects import Account as QB_Account
from account.models import Account
from quickbooks.objects.base import LinkedTxn
from quickbooks.objects import Invoice as QB_Invoice


class Payment(models.Model):
    class Meta:
        permissions = [
            ("can_view_summaries", "can view payment summaries"),
            ("can_add_fees_payments", "Can add fees payments")
        ]

    """this model represents a payment made for an invoice"""
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=None)
    date_paid = models.DateField(default=None, null=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, null=True, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=255, null=True,
                            default="Single Payment")
