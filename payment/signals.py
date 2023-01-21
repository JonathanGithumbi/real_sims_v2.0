from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Payment as InvoicePayment


@receiver(post_delete, sender=InvoicePayment)
def invoicepayment_postdelete_receiver(sender, instance, **kwargs):
    try:
        # update the balance record after every invoice item is deleted

        # increase the balance on the invoice
        inv = instance.invoice
        inv.balance += instance.amount
        inv.save()
        # the balance record should also be modified
        from invoice.models import BalanceTable
        record = BalanceTable.objects.get(student=instance.student)
        record.balance += instance.amount
        record.save()
    except:
        print("Done ")


@receiver(post_save, sender=InvoicePayment)
def invoicepayment_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        # after you make a payment, the balance on the invoice goes down
        invoice = instance.invoice
        invoice.balance -= instance.amount
        invoice.save()
        # the balance record should also go down
        from invoice.models import BalanceTable
        record = BalanceTable.objects.get(student=instance.student)
        record.balance -= instance.amount
        record.save()
    else:
        # if payment has been edited
        invoice = instance.invoice
        invoice.balance -= instance.amount
        invoice.save()
        # the balance record should also go down
        from invoice.models import BalanceTable
        record = BalanceTable.objects.get(student=instance.student)
        record.balance -= instance.amount
        record.save()


@receiver(pre_save, sender=InvoicePayment)
def invoice_presave_receiver(sender, instance, **kwargs):
    if instance.id is None:  # if this is a new instance
        print("invoice presave called")
    else:  # if this is an update to  an existing payment
        # if updating payments
        prev_payment = InvoicePayment.objects.get(pk=instance.pk)
        prev_amount = prev_payment.amount
        # revert payment on invoice and let the post save increase the balance again
        inv = instance.invoice
        inv.balance += prev_amount
        inv.save()
        # the balance record should also be modified
        from invoice.models import BalanceTable
        record = BalanceTable.objects.get(student=instance.student)
        record.balance += prev_amount
        record.save()
