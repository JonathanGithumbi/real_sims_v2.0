from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import BillItem, BillPayment

# Bill item signals

# billitem post save


@receiver(post_save, sender=BillItem)
def billitem_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        # When a new billitem is created, set its balance = its total
        instance.amount_due = instance.total
        instance.save()

    else:
        pass


# bill payment post save
@receiver(pre_save, sender=BillPayment)
def billpayment_presave_receiver(sender, instance, **kwargs):
    if instance.id is None:
        # if this is a new instance
        pass
    else:
        # if this is an existing instance being updated
        # if bill payment's amount is altered
        curr_obj = BillPayment.objects.get(id=instance.id)
        if instance.amount != curr_obj.amount:
            billitem = curr_obj.billitem
            #undo the current object's payment
            billitem.amount_due += curr_obj.amount
            billitem.save()


@receiver(post_save, sender=BillPayment)
def billpayment_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        # when a billpayment is created, devrease its billitem amount_due
        billitem = instance.billitem
        billitem.amount_due -= instance.amount
        billitem.save()
    else:
        billitem = instance.billitem
        billitem.amount_due -= instance.amount
        billitem.save()


@receiver(post_delete, sender=BillPayment)
def billpayment_postdelete_receiver(sender, instance, **kwargs):
    try:
        # increase the amount due whenever a payment is deleted
        billitem = instance.billitem
        billitem.amount_due += instance.amount
        billitem.save()

    except:
        print("There was an error deleting a billpayyment")
