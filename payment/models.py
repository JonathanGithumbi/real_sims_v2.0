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
        permissions=[
            ("can_view_summaries","can view payment summaries")
        ]

    """this model represents a payment made for an invoice"""
    # This models is for making payments for invoices.
    amount = models.DecimalField(max_digits=8, decimal_places=2,null=True, default=None)
    date_paid = models.DateField(default=None, null=True)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    synced = models.BooleanField(default=False, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,null=True, default=None)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,default=None)
    note = models.CharField(max_length=255,null=True,default="Single Payment")
    created = models.DateTimeField(auto_now_add=True,null=True)


    def create_qb_payment(self):
        access_token_obj = Token.objects.get(name='access_token')
        refresh_token_obj = Token.objects.get(name='refresh_token')
        realm_id_obj = Token.objects.get(name='realm_id')
        #create an auth_client
        auth_client = AuthClient(
            client_id = settings.CLIENT_ID,
            client_secret = settings.CLIENT_SECRET,
            access_token = access_token_obj.key,
            environment=settings.ENVIRONMENT,
            redirect_uri = settings.REDIRECT_URI
        )
        #create a quickboooks client
        client = QuickBooks(
            auth_client = auth_client,
            refresh_token = refresh_token_obj.key,
            company_id = realm_id_obj.key
        )
        #Generate the object's attributes
        #TotalAmt > self.amount
        #CustomerRef
        customer_qb_id = self.student.qb_id
        customer_obj = Customer.get(customer_qb_id,qb=client)
        # deposit to account ref
        dep_acc = Account.objects.get(name='invoice_payments_account')
        qb_dep_acc_obj = QB_Account.get(dep_acc.qb_id,qb=client)

        # acc receivable 
        acc_rec = Account.objects.get(name='invoices_account')
        qb_acc_rec_obj = QB_Account.get(acc_rec.qb_id, qb=client)
        # First create the qb_payment_obj 
        qb_payment_obj = QB_Payment()

        #create the qb_invoice
        qb_invoice_obj = QB_Invoice.get(self.invoice.qb_id,qb=client)
        #Create the linked txn
        linked_invoice = LinkedTxn()
        linked_invoice.TxnId = qb_invoice_obj.Id
        linked_invoice.TxnType='Invoice'
        #now for the line object
        payment_line_obj = PaymentLine()
        payment_line_obj.Amount = self.amount
        payment_line_obj.LinkedTxn.append(linked_invoice)

        # Apply attributes
        qb_payment_obj.TotalAmt = self.amount
        qb_payment_obj.CustomerRef = customer_obj.to_ref()
        qb_payment_obj.DepositToAccountRef=qb_dep_acc_obj.to_ref()
        qb_payment_obj.ARAccountRef = qb_acc_rec_obj.to_ref()
        qb_payment_obj.Line.append(payment_line_obj)
        #Save the object
        qb_payment_obj.save(qb=client)
        #return the object
        return qb_payment_obj

