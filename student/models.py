from django.db import models
from grade.models import Grade
from . import utils
class Student(models.Model):
    admission_number = models.CharField(max_length=30, null=True,default=None)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True )
    grade_admitted_to = models.ForeignKey(Grade, on_delete=models.CASCADE,related_name='grade_admitted_to')
    current_grade = models.ForeignKey(Grade, on_delete=models.CASCADE,blank=True,null=True)
    date_of_admission = models.DateField(auto_now_add=True)
    primary_contact_name = models.CharField(max_length = 255)
    primary_contact_phone_number = models.CharField(max_length = 255,blank=True)
    secondary_contact_name = models.CharField(max_length = 255)
    secondary_contact_phone_number = models.CharField(max_length = 255,blank=True)
    synced = models.BooleanField(default=False)
    # optionals 
    hot_lunch = models.BooleanField(default=False)
    transport = models.BooleanField(default=False)
    transport_fee = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name+' '+self.last_name

    

    