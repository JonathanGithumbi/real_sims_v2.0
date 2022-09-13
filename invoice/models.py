from calendar import calendar
from django.db import models
from fees_structure.models import TERM_CHOICES
from grade.models import Grade
import invoice
from student.models import Student

from quickbooks.objects import Invoice as QB_Invoice
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects import Item as QB_Item
from quickbooks.objects import Customer
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from item.models import Item as sales_item
from fees_structure.models import FeesStructure
from academic_calendar.models import AcademicCalendar

INVOICE_STATUS = [
    ("paid", "paid"),
    ('part-paid', 'part-paid'),
    ('unpaid', 'unpaid')
]

TERM_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3)
]


class InvoiceNumber(models.Model):
    """Generates the invoice number from instance's id attribute """
    """should it be linked to qb_invoice invoice number."""

    def __init__(self):
        pass

    created = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    """This is the invoice that has invoice items within it"""
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)  # added in views
    created = models.DateField(auto_now_add=True)  # created on save()
    year = models.IntegerField(null=True, default=None)  # added in views
    term = models.IntegerField(null=True, default=None)  # added in views
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True,
                                 default=None)  # to be added in registration views
    invoice_number = models.BigIntegerField(null=True, default=None)  # added in save
    invoice_number_formatted = models.CharField(max_length=255, default=None, null=True)  # added in save
    synced = models.BooleanField(default=False)  # added in save
    paid_status = models.BooleanField(default=False, null=True)  # updated when creating payments
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=None,
                                  null=True)  # hOW MUCH IS LEFT ON THE PAYMENT
    qb_id = models.CharField(max_length=255, null=True, default=None)

    def create_qb_invoice(self):
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
        # create the invoice obj
        qb_invoice_obj = QB_Invoice()

        # Populate the CustomerRef
        # get qb customer
        customer = Customer.get(id=self.student.qb_id, qb=client)
        # populate CustomerRef
        qb_invoice_obj.CustomerRef = customer.to_ref()

        # Add lines to invoice obj
        # get the items sold
        items = self.student.get_items()
        # iterate through each item to create a line
        for item in items:
            # create a line line detail to go into the line
            sales_item_line_detail = SalesItemLineDetail()

            # Populate line detail's ItemRef
            # get local item obj
            item_obj = sales_item.objects.get(name=item)
            # get qb item obj
            qb_item_obj = QB_Item.get(id=item_obj.qb_id, qb=client)
            # assign ItemRef
            sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
            # populate line detail quantity
            sales_item_line_detail.Qty = 1
            # populate the line detail's unit price - to be determined from the fees structure
            calendar_obj = AcademicCalendar()
            current_grade = self.student.current_grade
            term = calendar_obj.get_term()
            fee_structure_obj = FeesStructure.objects.get(item=item_obj, grade=current_grade, term=term)
            sales_item_line_detail.UnitPrice = fee_structure_obj.amount

            # create line
            sales_item_line = SalesItemLine()
            sales_item_line.SalesItemLineDetail = sales_item_line_detail
            sales_item_line.Amount = fee_structure_obj.amount
            sales_item_line.Description = item

            qb_invoice_obj.Line.append(sales_item_line)

        saved_qb_invoice = qb_invoice_obj.save(qb=client)
        return saved_qb_invoice

    def update_qb_invoice(self, item):
        # Reflect changes in the quickbooks by sparse updating the invoice
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
        # Get qb_invoice
        qb_invoice_obj = QB_Invoice.get(self.qb_id, qb=client)
        # Add a sales itemline for lunch
        # create a line line detail to go into the line
        sales_item_line_detail = SalesItemLineDetail()

        # Populate line detail's ItemRef

        # get qb item obj
        qb_item_obj = QB_Item.get(id=item.qb_id, qb=client)
        # assign ItemRef
        sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
        # populate line detail quantity
        sales_item_line_detail.Qty = 1
        # populate the line detail's unit price - to be determined from the fees structure
        calendar_obj = AcademicCalendar()
        current_grade = self.student.current_grade
        term = calendar_obj.get_term()
        fee_structure_obj = FeesStructure.objects.get(item=item, grade=current_grade, term=term)
        sales_item_line_detail.UnitPrice = fee_structure_obj.amount

        # create line
        sales_item_line = SalesItemLine()
        sales_item_line.SalesItemLineDetail = sales_item_line_detail
        sales_item_line.Amount = fee_structure_obj.amount
        sales_item_line.Description = item.name

        qb_invoice_obj.Line.append(sales_item_line)

        # save the invoice
        qb_invoice_obj.save(qb=client)
        return qb_invoice_obj

    def get_term(self):
        academic_calendar_obj = AcademicCalendar()
        term = academic_calendar_obj.get_term(self.created)
        return term

    def get_year(self):
        return self.created.year

    def get_amount(self):
        amount = 0
        local_item_objects = Item.objects.filter(invoice=self)
        for obj in local_item_objects:
            amount = obj.amount + amount

        return amount

    def get_amount_paid(self):
        amount_paid = self.amount - self.balance
        return amount_paid

    def format_invoice_no(self):
        return 'inv' + str(self.invoice_number).zfill(4)

    def save(self, *args, **kwargs):
        """Save is not called when you use the Models.update() so this is safe to use for registration"""
        inv_number = InvoiceNumber()
        inv_number.save()
        self.invoice_number = inv_number.id
        self.invoice_number_formatted = self.format_invoice_no()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Item(models.Model):
    """These are invoice items. i.e the items that compose the invoice"""
    # item_description = models.CharField(max_length=255,null=True,default=None)
    invoice_item = models.ForeignKey(sales_item, on_delete=models.DO_NOTHING, null=True, default=None)
    amount = models.IntegerField(null=True, default=None)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    created = models.DateField(null=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

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
