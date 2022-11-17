from datetime import datetime
from http import client
from venv import create
from django.db import models
from regex import E
from urllib3 import Retry
from grade.models import Grade

#from quickbooks.objects import Customer
from quickbooks import QuickBooks
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException

from QBWEBSERVICE.models import QBDModelMixin


class AdmissionNumber(models.Model):
    """Generates the unformatted admission number"""
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

# inherit the QBDModelMixin to the model that you want to sync with QB


class Student(QBDModelMixin):
    """this model represents a student enrolled in school"""

    class Meta:
        ordering = ['-date_of_admission']

    admission_number = models.IntegerField(null=True, default=None)
    admission_number_formatted = models.CharField(
        max_length=255, default=None, null=True)
    name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    grade_admitted_to = models.ForeignKey(
        Grade, on_delete=models.CASCADE, related_name='grade_admitted_to')
    current_grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, blank=True, null=True)
    date_of_admission = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    primary_contact_name = models.CharField(max_length=255)
    primary_contact_phone_number = models.CharField(max_length=255, blank=True)
    secondary_contact_name = models.CharField(max_length=255)
    secondary_contact_phone_number = models.CharField(
        max_length=255, blank=True)

    # This active flag defines whether or not the student gets  invoiced
    active = models.BooleanField(null=True, default=True)

    # optionals
    lunch = models.BooleanField(default=False)
    transport = models.BooleanField(default=False)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("student_profile", kwargs={"student_id": self.id})

    def format_adm_no(self):
        return 's' + str(self.admission_number).zfill(4)

    def get_items(self):
        """These are the compulsory recurring items for continuing students"""
        items = ['Tuition', 'Computer Lessons']

        return items

    def student_is_upper_class(self):
        LOWER_CLASSES = ['Grade 1', 'Grade 2', 'Grade 3',
                         'Pre Primary 1', 'Pre Primary 2', 'Play Group']
        if self.current_grade.title in LOWER_CLASSES:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        # saves the model to the Db
        # Generate admission number
        self.adm_no = AdmissionNumber()
        self.adm_no.save()
        # Assign the admission number object to the model's admission number
        self.admission_number = self.adm_no.id
        self.admission_number_formatted = self.format_adm_no()

        # Assign Initial Grade
        self.current_grade = self.grade_admitted_to

        super().save(*args, **kwargs)  # Call the "real" save() method.

       # implement thee 2 methods: to_qbd_obj() and from_qbd_obj
    @classmethod
    def to_qbd_obj(self, **fields):
        from QBWEBSERVICE.objects import Customer as QBCustomer
        # map your fields to the qbd_obj fields
        return QBCustomer(
            Name=self.__str__(),
            Phone=self.primary_contact_phone_number,
            AltPhone=self.secondary_contact_phone_number,
            Contact=self.primary_contact_name,
            AltContact=self.secondary_contact_name,

        )

    @classmethod
    def from_qbd_obj(cls, qbd_obj):
        # map qbd_obj fields to your model fields
        return cls(
            name=qbd_obj.Name,
            primary_contact_phone=qbd_obj.Phone,
            secondary_contact_phone=qbd_obj.AltPhone,
            primary_contact_name=qbd_obj.Contact,
            secondar_contact_name=qbd_obj.AltContact,
            qbd_object_id=qbd_obj.ListID,
            qbd_object_version=qbd_obj.EditSequence
        )

    # def update_qb_customer(self, student):
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
    #    customer = Customer.get(student.qb_id, qb=client)
    #    customer.DisplayName = student.first_name + ' ' + \
    #        student.middle_name + ' ' + student.last_name
#
    #    customer.save(qb=client)
    #    return customer

# def create_qb_customer(self):
    #    # create customer
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
#
    #    customer = Customer()
    #    customer.DisplayName = self.first_name + ' ' + \
    #        self.middle_name + ' ' + self.last_name
    #    saved_customer = customer.save(qb=client)
    #    return saved_customer
