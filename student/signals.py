from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Student
from academic_calendar.CalendarManager import CalendarManager
from invoice.InvoiceManager import InvoiceManager
from invoice.models import BalanceTable
from item.ItemManager import ItemManager
from invoice.models import Invoice
from invoice.models import Item as InvoiceItem
from fees_structure.models import BillingItem
# pre_save signal to populate missing fields


@receiver(pre_save, sender=Student)
def student_presave_receiver(sender, instance: Student, **kwargs):
    # if instance/row is being created, then do something
    if instance.id is None:  # id=None means it is a newobject
        # Populate Rows
        instance.current_grade = instance.grade_admitted_to
        cal = CalendarManager()
        instance.year_admitted = cal.get_year()
        instance.term_admitted = cal.get_term()
        instance.current_term = cal.get_term()
        instance.current_year = cal.get_year()
    else:
        # in case of update invoice/ uninvoice lunch/transport
        previous = Student.objects.get(id=instance.id)
        if instance.lunch != previous.lunch:
            if instance.lunch == True:
                # student subscribed to lunch
                # charge student for lunch on the current invoice
                item_manager = ItemManager()
                lunch_sales_item = item_manager.get_lunch_item()
                lunch_billing_item = BillingItem.objects.get(
                    item=lunch_sales_item, grades__in=[instance.current_grade])
                InvoiceItem.objects.create(
                    billing_item=lunch_billing_item,
                    invoice=Invoice.objects.filter(student=instance).latest()
                )
            else:
                item_manager = ItemManager()
                lunch_sales_item = item_manager.get_lunch_item()
                lunch_item = BillingItem.objects.get(
                    item=lunch_sales_item, grades__in=[instance.current_grade])
                invoice = Invoice.objects.filter(student=instance).latest()
                lunch_inv_item = InvoiceItem.objects.get(
                    invoice=invoice, billing_item=lunch_item)
                lunch_inv_item.delete()
        if instance.transport != previous.transport:
            if instance.transport == True:
                item_manager = ItemManager()
                transport_sales_item = item_manager.get_transport_item()
                transport_item = BillingItem.objects.get(
                    item=transport_sales_item, grades__in=[instance.current_grade])
                InvoiceItem.objects.create(
                    billing_item=transport_item,
                    invoice=Invoice.objects.filter(student=instance).latest()
                )
            else:
                item_manager = ItemManager()
                transport_sales_item = item_manager.get_transport_item()
                transport_item = BillingItem.objects.get(
                    item=transport_sales_item, grades__in=[instance.current_grade])
                invoice = Invoice.objects.filter(student=instance).latest()
                transport_inv_item = InvoiceItem.objects.get(
                    invoice=invoice, billing_item=transport_item)
                transport_inv_item.delete()


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
        inv_man.invoice_new_student(instance)

    else:
        print("error in student post save receiver")
