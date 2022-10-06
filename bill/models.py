from unicodedata import decimal
from django.db import models
from django import utils

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


class Bill(models.Model):

    bill_number = models.CharField(max_length=30, null=True, default=None, unique=True)
    created = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, default=None)
    synced = models.BooleanField(default=False)


    def __str__(self):
        return self.bill_number


PAYMENT_STATUS = [
    ('Fully Paid', 'Fully Paid'),
    ('Partly Paid', 'Partly Paid'),
    ('Unpaid', 'Unpaid')
]


class BillItem(models.Model):
    class Meta:
        permissions = [
            ("can_create_bill", "can create the bill"),
            ("can_edit_bill", "can edit the bill"),
            ("can_view_bill", "can view the bill"),
            ("can_delete_bill", "can delete the bill"),
            ("can_pay_bill", "can pay the bill")
        ]
    """This model represents a bill item from a third party vendor,"""
    """This bill records the bills that the school incurs, or the models records the money going out of the school 
    for any purpose."""
    """A bill is created whenever third party services are rendered"""
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING, null=True, default=None)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_per_quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    synced = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    fully_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def update_qb_bill(self):
        pass

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
