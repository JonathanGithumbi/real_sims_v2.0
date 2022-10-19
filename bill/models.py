
from email.policy import default
from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models
from django import utils
from sqlalchemy import null


from vendor.models import Vendor
from quickbooks.objects import Bill as qb_bill
from quickbooks.objects.base import Ref
from quickbooks.objects.detailline import DetailLine, AccountBasedExpenseLineDetail, AccountBasedExpenseLine

from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks import QuickBooks
from user_account.models import Token
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Vendor as qb_vendor
from quickbooks.objects import Account as qb_account
from account.models import Account
from user_account.models import User


class Bill(models.Model):

    bill_number = models.CharField(
        max_length=30, null=True, default=None, unique=True)
    created = models.DateField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, default=None)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.bill_number


PAYMENT_STATUS = [
    ('Fully Paid', 'Fully Paid'),
    ('Partly Paid', 'Partly Paid'),
    ('Unpaid', 'Unpaid')
]


class PettyCash(models.Model):
    balance = models.IntegerField(default=0)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.balance


class BillItem(models.Model):
    """This is a table for petty cash bill items"""
    """every row in this table is a transaction that affects the petty cash balance ; the transaction may increase the balance such as a deposit or could decrease the balance such as a bill item"""
    CATEGORY_CHOICES = [

        ("Office Supplies", "Office Supplies"),
        ("Teaching Reources", "Teaching Resources"),
        ("Deposit", "Deposit")
    ]

    class Meta:
        permissions = [
            ("can_create_a_bill", "can create local bill"),
            ("can_edit_bill", "can edit the bill"),
            ("can_view_bill", "can view the bill"),
            ("can_delete_bill", "can delete the bill"),
            ("can_pay_bill", "can pay the bill"),
            ("can_view_summaries", "Can view bill summaries"),
            ("can_topup_pettycash", "Can Topup Petty Cash")
        ]
    """This model represents a bill item from a third party vendor,"""
    """This bill records the bills that the school incurs, or the models records the money going out of the school 
    for any purpose."""
    """A bill is created whenever third party services are rendered"""

    category = models.CharField(
        max_length=22, choices=CATEGORY_CHOICES, default=None, null=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_per_quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    # this balance represents the petty cash balance that remained after the addition of this item, like a snapshot of the balance in time
    balance = models.IntegerField(default=0, null=True)
    recipient = models.CharField(max_length=255, null=True, default="")
    synced = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    fully_paid = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, default=None)

    def __str__(self):
        return self.description

    def create_qb_bill(self):
        access_token_obj = Token.objects.get(name='access_token')
        refresh_token_obj = Token.objects.get(name='refresh_token')
        realm_id_obj = Token.objects.get(name='realm_id')
        # create an auth_client
        auth_client = AuthClient(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            access_token=access_token_obj.key,
            environment=settings.ENVIRONMENT,
            redirect_uri=settings.REDIRECT_URI
        )
        # create a quickboooks client
        client = QuickBooks(
            auth_client=auth_client,
            refresh_token=refresh_token_obj.key,
            company_id=realm_id_obj.key
        )
        # Bill Object
        bill = qb_bill()

        # get vendor
        qb_vendor_obj = qb_vendor.get(self.vendor.qb_id, qb=client)
        # create Vendor Ref
        vendor_ref = qb_vendor_obj.to_ref()
        bill.VendorRef = vendor_ref

        # get Account
        sims_acc_obj = Account.objects.get(name="KINGS EDU CENTRE EXPENSES")

        qb_account_object = qb_account.get(sims_acc_obj.qb_id, qb=client)
        qb_account_object_ref = qb_account_object.to_ref()
        # Line
        acc_based_expense_line = AccountBasedExpenseLine()
        acc_based_expense_line.Amount = self.total
        acc_based_expense_line.Description = self.description
        acc_based_expense_line_detail = AccountBasedExpenseLineDetail()
        acc_based_expense_line_detail.AccountRef = qb_account_object_ref
        acc_based_expense_line.AccountBasedExpenseLineDetail = acc_based_expense_line_detail
        bill.Line.append(acc_based_expense_line)
        saved_bill = bill.save(qb=client)
        return saved_bill

    def retrieve_qb_bill(self):
        pass

    def update_qb_bill(self):
        pass

    def delete_qb_bill(self):
        pass

    def pay_bill(self, bill_payment_obj):
        bill_obj = self
        qb_bill_payment_obj = bill_payment_obj.create_qb_bill_payment_obj(self)

        return bill_payment_obj

    def get_petty_cash_balance(self):
        return self.petty_cash_balance
