from django.db import models
from fees_structure.models import TERM_CHOICES
from grade.models import Grade
import invoice
from student.models import Student

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
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id


class Invoice(models.Model):
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    grade = models.ForeignKey(Grade,on_delete=models.DO_NOTHING)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField()
    status = models.CharField(max_length=255, choices=INVOICE_STATUS,default='unpaid')
    invoice_number = models.ForeignKey(InvoiceNumber,on_delete=models.CASCADE,default=None,null=True)
    invoice_number_formatted = models.CharField(max_length=255,default=None,null=True)
    synced = models.BooleanField(default=False)


    def get_amount(self):
        invoice = Invoice.objects.get(pk=self.id)
        items = invoice.item_set.all()
        amount = 0
        for item in items:
            amount += item.amount
        return amount


        

    def format_invoice_no(self,invoice_no):
        return 'inv'+str(invoice_no).zfill(4)

    def save(self, *args, **kwargs):
        inv_number = InvoiceNumber()
        inv_number.save()
        self.invoice_number = inv_number
        inv_no_id = inv_number.id
        self.invoice_number_formatted = self.format_invoice_no(inv_no_id)
        super().save(*args, **kwargs)  # Call the "real" save() method.



    
class Item(models.Model):
    item_description = models.CharField(max_length=255,choices=ITEM_CHOICES,null=True,default=None)
    amount = models.IntegerField(null=True,default=None)
    synced= models.BooleanField(default=False)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)


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

