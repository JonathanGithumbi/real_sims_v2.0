
from calendar import calendar
from django.db import models
from fees_structure.models import TERM_CHOICES
from grade.models import Grade
import invoice
from student.models import Student

from quickbooks.objects import Invoice as qb_invoice
from quickbooks.objects.detailline import SalesItemLine,SalesItemLineDetail
from quickbooks.objects import Item as qb_item
from quickbooks.objects import Customer
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from item.models import Item as sales_item
from fees_structure.models import FeesStructure
from academic_calendar.models import AcademicCalendar

INVOICE_STATUS=[
    ("paid","paid"),
    ('part-paid','part-paid'),
    ('unpaid','unpaid')
]

#this list contains all of the possible charges that could be levied to a student
ITEM_CHOICES = [
    ("admission","admission"),
    ('diary_and_report_book','diary_and_report_book'),
    ('interview_fee_lower_classes','interview_fee_lower_classes'),
    ('interview_fee_upper_classes','interview_fee_upper_classes'),
    ('tuition','tuition'),
    ('computer_lessons','computer_lessons'),
    ('transport','transport'),
    ('lunch','lunch')
]
TERM_CHOICES = [ 
    (1,1),
    (2,2),
    (3,3)
]

class InvoiceNumber(models.Model):
    """Generates the invoice number """
    created = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=INVOICE_STATUS,default='unpaid')
    invoice_number = models.BigIntegerField(null=True,default=None)
    invoice_number_formatted = models.CharField(max_length=255,default=None,null=True)
    synced = models.BooleanField(default=False)
    qb_id = models.CharField(max_length=255,null=True, default=None)
    

    def create_invoice(self):
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
        #create the invoice obj
        qb_invoice_obj = qb_invoice()

        #Populate the CustomerRef
            #get qb customer
        customer = Customer.get(id=self.student.qb_id, qb=client)
            #populate CustomerRef
        qb_invoice_obj.CustomerRef = customer.to_ref()

        #Add lines to invoice obj
            #get the items sold
        items = self.student.get_items()
            #iterate through each item to create a line
        for item in items:

            #create a line line detail to go into the line
            sales_item_line_detail = SalesItemLineDetail()

            #Populate line detail's ItemRef
                #get local item obj
            item_obj = sales_item.objects.get(name = item)
                #get qb item obj 
            qb_item_obj =  qb_item.get(id=item_obj.qb_id,qb=client)
                #assign ItemRef
            sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
            #populate line detail quantity
            sales_item_line_detail.Qty = 1
            #populate the line detail's unit price - to be determined from the fees structure
            calendar_obj = AcademicCalendar()
            fee_structure_obj = FeesStructure.objects.get(item = item_obj,grade=self.student.current_grade,term=calendar_obj.get_term())
            sales_item_line_detail.UnitPrice = fee_structure_obj.amount

            #create line 
            sales_item_line = SalesItemLine()
            sales_item_line.SalesItemLineDetail = sales_item_line_detail
            sales_item_line.Amount = self.get_amount()
            sales_item_line.Description = item

            qb_invoice_obj.Line.append(sales_item_line)

        saved_invoice = qb_invoice_obj.save(qb=client)
        return saved_invoice


    def get_amount(self):
        items = self.student.get_items()
        amount = 0
        for item in items:
            item_obj = sales_item.objects.get(name=item)
            calendar_obj = AcademicCalendar()
            fee_structure_obj = FeesStructure.objects.get(item=item_obj,term = calendar_obj.get_term(),grade = self.student.current_grade)
            total = amount + fee_structure_obj.amount

        return total


    def format_invoice_no(self):
        return 'inv'+str(self.invoice_number).zfill(4)

    def save(self, *args, **kwargs):
        inv_number = InvoiceNumber()
        inv_number.save()
        self.invoice_number = inv_number.id
        self.invoice_number_formatted = self.format_invoice_no()
        saved_invoice = self.create_invoice()
        self.synced = True
        self.qb_id = saved_invoice.Id
        super().save(*args, **kwargs)  # Call the "real" save() method.



    
class Item(models.Model):
    item_description = models.CharField(max_length=255,choices=ITEM_CHOICES,null=True,default=None)
    amount = models.IntegerField(null=True,default=None)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        pass


class BalanceTable(models.Model):
    """This table reflects the accumulation of all of a students amount owed to the school
    this table is updated whenever a payment is made and whenever an invoice is created
    this table should not allow deletion of a student if they;re balance is not 0
    wheneve the invoice is added, the amoun is added to the balance 
    whenever a payment is made, the amount is deducted from the balance 
    allows negative numbers to iindicate overpayment
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    modified = models.DateTimeField(auto_now=True)

