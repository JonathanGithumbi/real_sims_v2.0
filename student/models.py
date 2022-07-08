from datetime import datetime
from venv import create
from django.db import models
from grade.models import Grade

class AdmissionNumber(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Student(models.Model):
    admission_number = models.ForeignKey(AdmissionNumber,on_delete=models.CASCADE,default=None,null=True)
    admission_number_formatted = models.CharField(max_length=255,default=None,null=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True )
    grade_admitted_to = models.ForeignKey(Grade, on_delete=models.CASCADE,related_name='grade_admitted_to')
    current_grade = models.ForeignKey(Grade, on_delete=models.CASCADE,blank=True,null=True)
    date_of_admission = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
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

    def format_adm_no(self,adm_no):
        return 's'+str(adm_no).zfill(4)

    def save(self, *args, **kwargs):
        self.adm_no = AdmissionNumber()
        self.adm_no.save()
        self.admission_number = self.adm_no
        self.adm_no_id = self.adm_no.id
        self.admission_number_formatted = self.format_adm_no(self.adm_no_id)
        self.current_grade = self.grade_admitted_to
        super().save(*args, **kwargs)  # Call the "real" save() method.
        
