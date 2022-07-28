from datetime import datetime
from http import client
from venv import create
from django.db import models
from regex import E
from grade.models import Grade
from quickbooks import QuickBooks
from quickbooks.objects import Customer

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException


class AdmissionNumber(models.Model):
    """Generates the unformatted admission number"""
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id



class Student(models.Model):
    class Meta:
        ordering = ['-date_of_admission']
    admission_number = models.IntegerField(null=True,default=None)
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
    lunch = models.BooleanField(default=False)
    transport = models.BooleanField(default=False)
    qb_id = models.CharField(max_length=20,null=True, default=None)
    
    def __str__(self):
        return self.first_name+' '+self.last_name

    def format_adm_no(self):
        return 's'+str(self.admission_number).zfill(4)

    def get_items(self):
        items = ['Tuition']
        if self.lunch:
            items.append('Lunch')
        if self.transport:
            items.append('Transport')

        return items

    def create_customer(self):
        #create customer
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
        
        customer = Customer()
        customer.DisplayName = self.first_name +' '+ self.middle_name +' '+ self.last_name
        saved_customer = customer.save(qb=client)
        return saved_customer
    

    def save(self, *args, **kwargs):

        #Generate admission number
        self.adm_no = AdmissionNumber()
        self.adm_no.save()
        self.admission_number = self.adm_no.id # Assign the admission number object to the model's admission number
        self.admission_number_formatted = self.format_adm_no()

        #Assign Initial Grade
        self.current_grade = self.grade_admitted_to
        
        #create & save customer 
        saved_customer = self.create_customer()

        #populate populate and save remaining fields
        self.synced = True
        self.qb_id = saved_customer.Id
        super().save(*args, **kwargs)  # Call the "real" save() method.
        
        

            


        
        