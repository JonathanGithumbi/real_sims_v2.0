from django.db.models import pre_save, post_save
from django.dispatch import receiver
from .models import Invoice
from .models import Item as InvoiceItem
from .models import BalanceTable


@receiver(post_save, sender=InvoiceItem)
def update_bal_record(sender, instance, created, **kwargs):
    # update the balance record after every invoice item is recorded
    if created:
        bal_rec = BalanceTable.objects.get(student=instance.invoice.student)
        bal_rec.balance += instance.amount
        bal_rec.save(update_fields=['balance'])



