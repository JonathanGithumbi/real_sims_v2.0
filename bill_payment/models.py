from django.db import models
from bill.models import BillItem
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks import QuickBooks
from user_account.models import Token
from quickbooks.exceptions import QuickbooksException
from vendor.models import Vendor
from quickbooks import QuickBooks
from quickbooks.objects import Customer

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.objects import BillPayment as QB_BillPayment
from quickbooks.objects import BillPaymentLine
from quickbooks.objects import Vendor as qb_vendor
from quickbooks.objects import Bill as qb_bill
from quickbooks.objects.base import LinkedTxn
from quickbooks.objects import Account as QB_Account

from account.models import Account as Local_Account
from quickbooks.objects.billpayment import CheckPayment

# Create your models here.


class BillPayment(models.Model):
    """This model represents a payment for a bill"""
    """BillPayment holds the records for the payment of bills, until the bill is completely paid for,severals bill 
    payments for one bill are to be expected."""  # Only if the software has a bill management feature.
    """But out of the box, this bill payment will only function to record full ayment of bills"""
    qb_id = models.CharField(max_length=255, null=True, default=None)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    # This is the amount paid for a particular period
    amount = models.IntegerField(null=True, default=0)
    bill = models.ForeignKey(BillItem, on_delete=models.DO_NOTHING)
    synced = models.BooleanField(null=True, default=None)

    def create_qb_bill_payment_obj(self):
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

        # get the qb_bill_item
        qb_bill_item = qb_bill.get(self.bill.qb_id, qb=client)

        # Linked Txn
        lnk_txn = LinkedTxn()
        lnk_txn.TxnId = qb_bill_item.Id
        lnk_txn.TxnType = 'Bill'

        # construct bill payment line
        bill_paym_line = BillPaymentLine()
        bill_paym_line.Amount = self.amount
        bill_paym_line.LinkedTxn.append(lnk_txn)
        # get vendor bject
        qb_vendor_obj = qb_vendor.get(self.vendor.qb_id, qb=client)
        # create qb bill payment object
        bill_paym_obj = QB_BillPayment()
        bill_paym_obj.VendorRef = qb_vendor_obj.to_ref()
        bill_paym_obj.TotalAmt = self.amount
        bill_paym_obj.Line.append(bill_paym_line)
        bill_paym_obj.PayType = "Check"
        # get qb_account
        # first get local
        local_qb_acc = Local_Account.objects.get(name='Checking Bank Account')
        qb_acc_obj = QB_Account.get(local_qb_acc.qb_id, qb=client)
        # create checkpayment object
        check_paym_obj = CheckPayment()
        check_paym_obj.BankAccountRef = qb_acc_obj.to_ref()
        bill_paym_obj.CheckPayment = check_paym_obj
        bill_paym_obj.save(qb=client)

        return bill_paym_obj
