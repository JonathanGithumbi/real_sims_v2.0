from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Student
from academic_calendar.CalendarManager import CalendarManager
from invoice.InvoiceManager import InvoiceManager
from invoice.models import BalanceTable
from item.ItemManager import ItemManager
from invoice.models import Invoice
from invoice.models import Item as InvoiceItem

# pre_save signal to populate missing fields


@receiver(pre_save, sender=Student)
def student_presave_receiver(sender, instance, **kwargs):
    # if instance/row is being created, then do something
    if instance.id is None:
        # Populate Rows
        instance.current_grade = instance.grade_admitted_to
        cal = CalendarManager()
        instance.year_admitted = cal.get_year()
        instance.term_admitted = cal.get_term()
        instance.current_term = cal.get_term()
        instance.current_year = cal.get_year()
    else:
        # instance is being modified
        pass


@receiver(post_save, sender=Student)
def student_postsave_receiver(sender, instance, created, **kwargs):
    # Create the balance table also
    if created:
        # only for a new student do you create a balance record
        BalanceTable.objects.create(
            student=instance
        )
        # invoice the student
        inv_man = InvoiceManager()
        try:
            inv_man.invoice_new_student(instance)
        except:
            print("something went wrong while invoicing a new student")
    else:
        # in case of update invoice/ uninvoice lunch/transport
        if instance.lunch == True:
            # student subscribed to lunch
            # charge student for lunch on the current invoice
            item_man = ItemManager()
            lunch_item = item_man.get_lunch_item()
            latest_invoice = Invoice.objects.filter(student=instance).latest()

        else:
            pass

        if instance.tranpsort == False:
            pass
        else:
            pass
