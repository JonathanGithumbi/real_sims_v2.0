from django.db import models
from fees_structure.models import TERM_CHOICES
from grade.models import Grade
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
class Invoice(models.Model):
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    grade = models.ForeignKey(Grade,on_delete=models.DO_NOTHING)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField()
    status = models.CharField(max_length=255, choices=INVOICE_STATUS,default='unpaid')
    invoice_number = models.CharField(max_length=255,null=True, default=None)
    synced = models.BooleanField(default=False)
    
class Item(models.Model):
    item = models.CharField(max_length=255,choices=ITEM_CHOICES)
    amount = models.IntegerField()
    synced= models.BooleanField(default=False)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)

