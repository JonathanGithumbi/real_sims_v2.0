from QBWEBSERVICE.models import QBDModelMixin
from calendar import calendar
from django.db import models
from fees_structure.models import TERM_CHOICES
from grade.models import Grade


from quickbooks.objects import Account as QB_Account
from quickbooks.objects import Invoice as QB_Invoice
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects import Item as QB_Item
from quickbooks.objects import Customer
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from item.models import Item as sales_item
from fees_structure.models import FeesStructureBatch
from academic_calendar.models import Year, Term
from student.models import Student


class Invoice(models.Model):
    """An Invoice. Charged to the active students at the beginning of every term."""
    class Meta:
        db_table = "Invoice_invoice"

    balance = models.IntegerField(null=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True)
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def status(self):
        if self.balance is None:
            return 'Not Fully Paid'
        if self.balance == 0:
            return 'Fully Paid'
        if self.balance < 0:
            return 'Overpaid'
        if self.balance > 0:
            return 'Not Fully Paid'

    def fully_paid(self):
        balance = self.get_balance()
        if balance != 0:
            return False
        if balance == 0:
            return True

    def get_term(self):
        return self.term

    def get_year(self):
        return self.year

    def get_total_amount(self):
        amount = 0
        items = Item.objects.filter(invoice=self)
        for item in items:
            amount = amount+item.amount

        return amount

    def get_amount_paid(self):
        payments = self.payment_set.filter(invoice=self)
        payment_amount = 0
        for payment in payments:
            payment_amount = payment_amount + payment.amount

        return payment_amount

    def get_balance(self):
        # amount-payment amount
        if self.balance is None:
            return self.get_total_amount()
        else:
            return self.balance


class Item(models.Model):
    """These are invoice items. i.e the items that compose the invoice"""
    """Whenever an invoice item is added to an invoice, the save method modifies the invoice by increasing the amount and balance of the invoice"""
    # item_description = models.CharField(max_length=255,null=True,default=None)
    sales_item = models.ForeignKey(
        sales_item, on_delete=models.DO_NOTHING, null=True, default=None)
    amount = models.IntegerField(null=True, default=None)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.invoice_item.name


class BalanceTable(models.Model):
    """This table reflects the accumulation of all of a students amount owed to the school
    this table is updated whenever a payment is made and whenever an invoice is created
    this table should not allow deletion of a student if they;re balance is not 0
    wheneve the invoice is added, the amoun is added to the balance 
    whenever a payment is made, the amount is deducted from the balance 
    Negative numbers mean that the student owes the school while positive numbers means that the school owes the student
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    modified = models.DateTimeField(auto_now=True)

    def increase_balance(self, amount):
        self.balance = self.balance + amount
        self.save()

    def decrease_balance(self, amount):
        self.balance = self.balance - amount
        self.save()

    def get_balance(self):
        return self.balance


#
    # def create_qb_invoice(self, items):
    #    access_token_obj = Token.objects.get(name='access_token')
    #    refresh_token_obj = Token.objects.get(name='refresh_token')
    #    realm_id_obj = Token.objects.get(name='realm_id')
    #    # create an auth_client
    #    auth_client = AuthClient(
    #        client_id=settings.CLIENT_ID,
    #        client_secret=settings.CLIENT_SECRET,
    #        access_token=access_token_obj.key,
    #        environment=settings.ENVIRONMENT,
    #        redirect_uri=settings.REDIRECT_URI
    #    )
    #    # create a quickboooks client
    #    client = QuickBooks(
    #        auth_client=auth_client,
    #        refresh_token=refresh_token_obj.key,
    #        company_id=realm_id_obj.key
    #    )
    #    # create the invoice obj
    #    qb_invoice_obj = QB_Invoice()
    #    income_account = QB_Account.get(id=123, qb=client)
    #    income_account_ref = income_account.to_ref()
    #    # Populate the CustomerRef
    #    # get qb customer
    #    customer = Customer.get(id=self.student.qb_id, qb=client)
    #    # populate CustomerRef
    #    qb_invoice_obj.CustomerRef = customer.to_ref()
    #    qb_invoice_obj.class_dict['DepositToAccountRef'] = income_account_ref
#
    #    # Add lines to invoice obj
    #    # get the items sold
#
    #    # iterate through each item to create a line
    #    for item in items:
    #        # create a line line detail to go into the line
    #        sales_item_line_detail = SalesItemLineDetail()
#
    #        # Populate line detail's ItemRef
    #        # get local item obj
    #        item_obj = sales_item.objects.get(name=item)
    #        # get qb item obj
    #        qb_item_obj = QB_Item.get(id=item_obj.qb_id, qb=client)
    #        # assign ItemRef
    #        sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
    #        # populate line detail quantity
    #        sales_item_line_detail.Qty = 1
    #        # populate the line detail's unit price - to be determined from the fees structure
    #        calendar_obj = AcademicCalendar()
    #        current_grade = self.student.current_grade
    #        term = calendar_obj.get_term()
    #        fee_structure_obj = FeesStructure.objects.get(
    #            item=item_obj, grade=current_grade, term=term)
    #        sales_item_line_detail.UnitPrice = fee_structure_obj.amount
#
    #        # create line
    #        sales_item_line = SalesItemLine()
    #        sales_item_line.SalesItemLineDetail = sales_item_line_detail
    #        sales_item_line.Amount = fee_structure_obj.amount
    #        sales_item_line.Description = item
#
    #        qb_invoice_obj.Line.append(sales_item_line)
#
    #    saved_qb_invoice = qb_invoice_obj.save(qb=client)
    #    return saved_qb_invoice

    # def update_qb_invoice(self, item):
    #    # Reflect changes in the quickbooks by sparse updating the invoice
    #    access_token_obj = Token.objects.get(name='access_token')
    #    refresh_token_obj = Token.objects.get(name='refresh_token')
    #    realm_id_obj = Token.objects.get(name='realm_id')
#
    #    # create an auth_client
    #    auth_client = AuthClient(
    #        client_id=settings.CLIENT_ID,
    #        client_secret=settings.CLIENT_SECRET,
    #        access_token=access_token_obj.key,
    #        environment=settings.ENVIRONMENT,
    #        redirect_uri=settings.REDIRECT_URI
    #    )
    #    # create a quickboooks client
    #    client = QuickBooks(
    #        auth_client=auth_client,
    #        refresh_token=refresh_token_obj.key,
    #        company_id=realm_id_obj.key
    #    )
    #    # Get qb_invoice
    #    qb_invoice_obj = QB_Invoice.get(self.qb_id, qb=client)
    #    # Add a sales itemline for lunch
    #    # create a line line detail to go into the line
    #    sales_item_line_detail = SalesItemLineDetail()
#
    #    # Populate line detail's ItemRef
#
    #    # get qb item obj
    #    qb_item_obj = QB_Item.get(id=item.qb_id, qb=client)
    #    # assign ItemRef
    #    sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
    #    # populate line detail quantity
    #    sales_item_line_detail.Qty = 1
    #    # populate the line detail's unit price - to be determined from the fees structure
    #    calendar_obj = AcademicCalendar()
    #    current_grade = self.student.current_grade
    #    term = calendar_obj.get_term()
    #    fee_structure_obj = FeesStructure.objects.get(
    #        item=item, grade=current_grade, term=term)
    #    sales_item_line_detail.UnitPrice = fee_structure_obj.amount
#
    #    # create line
    #    sales_item_line = SalesItemLine()
    #    sales_item_line.SalesItemLineDetail = sales_item_line_detail
    #    sales_item_line.Amount = fee_structure_obj.amount
    #    sales_item_line.Description = item.name
#
    #    qb_invoice_obj.Line.append(sales_item_line)
#
    #    # save the invoice
    #    qb_invoice_obj.save(qb=client)
    #    return qb_invoice_obj
# Obsolete Delete when possible
class InvoiceNumber(models.Model):
    """Generates the invoice number from instance's id attribute """
    """should it be linked to qb_invoice invoice number."""
    created = models.DateTimeField(auto_now_add=True)
