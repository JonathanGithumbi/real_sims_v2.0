from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Student
from academic_calendar.CalendarManager import CalendarManager
from invoice.InvoiceManager import InvoiceManager
from invoice.models import BalanceTable
# pre_save signal to populate missing fields


@receiver(pre_save, sender=Student)
def populate_attributes(sender, instance, **kwargs):
    # if instance/row is being created, then do something
    if instance.id is None:
        # Populate Rows
        instance.current_grade = instance.grade_admitted_to
        cal = CalendarManager()
        instance.year_admitted = cal.get_year()
        instance.term_admitted = cal.get_term()
        instance.current_term = cal.get_term()
        instance.current_year = cal.get_year()
        print("pre save mthod col")
    else:
        # instance is being modified
        pass


@receiver(post_save, sender=Student)
def invoice_new_student(sender, instance, created, **kwargs):
    # Create the balance table also
    if created:
        BalanceTable.objects.create(
            student=instance
        )
        # invoice the student
        inv_man = InvoiceManager()
        try:
            inv_man.invoice_new_student(instance)
        except:
            print("something went wrong while invoicing a new student")
