from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Invoice
from .models import Item as InvoiceItem
from .models import BalanceTable


@receiver(post_save, sender=InvoiceItem)
def invoiceitem_postsave_receiver(sender, instance, created, **kwargs):

    if created:
        # update the balance record after every invoice item is recorded
        bal_rec = BalanceTable.objects.get(student=instance.invoice.student)
        bal_rec.balance += instance.billing_item.amount
        bal_rec.save(update_fields=['balance'])

        # increase the balance on the invoice
        inv = instance.invoice
        inv.balance += instance.billing_item.amount
        inv.save()


@receiver(post_delete, sender=InvoiceItem)
def invoiceitem_postdelete_receiver(sender, instance, **kwargs):
    # update the balance record after every invoice item is deleted
    bal_rec = BalanceTable.objects.get(student=instance.invoice.student)
    bal_rec.balance -= instance.billing_item.amount
    bal_rec.save(update_fields=['balance'])

    # increase the balance on the invoice
    inv = instance.invoice
    inv.balance -= instance.billing_item.amount
    inv.save()
