from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Invoice
from .models import Item as InvoiceItem
from .models import BalanceTable
from django_quickbooks.models import QBDTask, ContentType
from django_quickbooks import QUICKBOOKS_ENUMS


#@receiver(post_save, sender=Invoice)
#def send_invoice_to_qbtask(sender, instance, created, **kwargs):
#    QBDTask.objects.create(
#        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
#        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
#        object_id=instance.id,
#        content_type=ContentType.objects.get_for_model(instance),
#        realm_id="c83de7e8-c6de-418b-88a9-4f30a5ff1cce"
#    )


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
    try:
        # update the balance record after every invoice item is deleted
        bal_rec = BalanceTable.objects.get(student=instance.invoice.student)
        bal_rec.balance -= instance.billing_item.amount
        bal_rec.save(update_fields=['balance'])

        # increase the balance on the invoice
        inv = instance.invoice
        inv.balance -= instance.billing_item.amount
        inv.save()
    except:
        print("Balance table not available ")


@receiver(pre_save, sender=Invoice)
def invoice_presave_receiver(sender, instance, **kwargs):
    if instance.id is None:
        print("invoice presave called")
