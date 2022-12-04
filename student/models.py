
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
from academic_calendar.models import Year, Term
from quickbooks.exceptions import QuickbooksException

from QBWEBSERVICE.models import QBDModelMixin


class AdmissionNumber(models.Model):
    """Generates the unformatted admission number"""
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Student(models.Model):
    """this model represents a student enrolled in school"""

    class Meta:
        ordering = ['-date_of_admission']
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    grade_admitted_to = models.ForeignKey(
        Grade, on_delete=models.CASCADE, related_name='grade_admitted_to')
    current_grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, blank=True, null=True)
    date_of_admission = models.DateField(auto_now_add=True, blank=True)
    year_admitted = models.ForeignKey(
        Year, on_delete=models.CASCADE, null=True, blank=True)
    term_admitted = models.ForeignKey(
        Term, on_delete=models.CASCADE, null=True, blank=True)
    current_term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name='current_term', null=True, blank=True)
    current_year = models.ForeignKey(
        Year, on_delete=models.CASCADE, related_name='current_year', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    primary_contact_name = models.CharField(max_length=255, blank=True)
    primary_contact_phone_number = models.CharField(max_length=255, blank=True)
    secondary_contact_name = models.CharField(max_length=255, blank=True)
    secondary_contact_phone_number = models.CharField(
        max_length=255, blank=True)

    # This active flag defines whether or not the student gets  invoiced
    active = models.BooleanField(null=True, default=True, blank=True)

    # This visible flag will determing whether the student is visible; an alternative to deleting data
    visible = models.BooleanField(null=True, default=True, blank=True)

    # optionals
    lunch = models.BooleanField(default=False, blank=True)
    transport = models.BooleanField(default=False, blank=True)

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
