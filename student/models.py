
from django.db import models

from grade.models import Grade

from academic_calendar.models import Year, Term

from fees_structure.BillingItemManager import BillingItemManager
from academic_calendar.CalendarManager import CalendarManager
from item.ItemManager import ItemManager
from fees_structure.models import BillingItem


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
    contact1_name = models.CharField(max_length=255, blank=True)
    contact1_number = models.CharField(max_length=255, blank=True)
    contact2_name = models.CharField(max_length=255, blank=True)
    contact2_number = models.CharField(
        max_length=255, blank=True)

    # This active flag defines whether or not the student gets  invoiced
    active = models.BooleanField(null=True, default=True, blank=True)

    # This visible flag will determing whether the student is visible; an alternative to deleting data
    visible = models.BooleanField(null=True, default=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_transport_status(self):
        latest_invoice = self.invoice_set.all().latest()
        bill_man = BillingItemManager()
        trans_bill = bill_man.get_trans_bill()
        if trans_bill in latest_invoice.item_set.all():
            return True
        else:
            return False

    def get_lunch_status(self):
        # get latest invoice

        latest_invoice = self.invoice_set.all().latest()
        bill_man = BillingItemManager()
        lunch_bill = bill_man.get_lunch_bill()
        if lunch_bill in latest_invoice.item_set.all():
            return True
        else:
            return False

    def get_fees_balance(self):
        from student.StudentManager import StudentManager
        man = StudentManager()
        return man.get_fees_balance(self)

    def get_fees_due(self):
        from invoice.models import BalanceTable
        bal_rec = BalanceTable.objects.get(student=self)
        return bal_rec.balance

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

    def is_taking_lunch(self):
        # check whether the student has been invoice for lunch in this term's invoice
        # get this term's invoice
        cal_man = CalendarManager()
        current_term = cal_man.get_term()

        current_invoice = self.invoice_set.get(term=current_term)

        # check if the lunch item is among the invoice's billing items
        item_man = ItemManager()
        lunch_item = item_man.get_lunch_item()
        # get the lunch billing item
        lunch_bill = BillingItem.objects.get(item=lunch_item)
        print(lunch_bill in current_invoice.item_set.all())

        for item in current_invoice.item_set.all():
            if item.billing_item == lunch_bill:
                return True
        else:
            return False

    def is_taking_transport(self):

        # check whether the student has been invoice for transport in this term's invoice
        # get this term's invoice
        cal_man = CalendarManager()
        current_term = cal_man.get_term()

        current_invoice = self.invoice_set.get(term=current_term)

        # check if the transport item is among the invoice's billing items
        item_man = ItemManager()
        transport_item = item_man.get_transport_item()
        # get the transport billing item
        transport_bill = BillingItem.objects.get(item=transport_item)
        print(transport_bill in current_invoice.item_set.all())

        for item in current_invoice.item_set.all():
            if item.billing_item == transport_bill:
                return True
        else:
            return False
