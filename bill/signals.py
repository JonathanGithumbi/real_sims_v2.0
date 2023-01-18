from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import BillItem, BillPayment, CashTransaction
from .CashManager import CashManager


# CASH TRANSACTION SIGNALS
@receiver(pre_delete, sender=CashTransaction)
def cashtransaction_predelete_receiver(sender, instance, **kwargs):
    # unapply deposit action
    if instance.operation == 'Deposit':
        cash_man = CashManager()
        cash_man.decrease_petty_cash_balance(instance.amount)


@receiver(pre_save, sender=CashTransaction)
def cashtransaction_presave_receiver(sender, instance: CashTransaction, **kwargs):
    if instance.id is None:
        pass
    else:
        if instance.operation == 'Deposit':
            current_obj = CashTransaction.objects.get(id=instance.id)
            cash_man = CashManager()
            cash_man.decrease_petty_cash_balance(current_obj.amount)


@receiver(post_save, sender=CashTransaction)
def cashtransaction_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        if instance.operation == 'Deposit':
            # if a deposiit is made, increase the balance
            cash_man = CashManager()
            cash_man.increase_cash_balance(instance.amount)
        if instance.operation == 'Withdraw':
            pass
    else:  # if updated(i'm currenctly not allowing the user alter withdraw operations directly.)
        if instance.operation == 'Deposit':
            cash_man = CashManager()
            cash_man.increase_cash_balance(instance.amount)
        if instance.operation == 'Withdraw':
            pass


# BILL ITEM SIGNALS
@receiver(post_save, sender=BillItem)
def billitem_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        pass

    else:
        pass


@receiver(pre_save, sender=BillItem)
def billitem_presave_receiver(sender, instance: BillItem, **kwargs):
    if instance.id is None:
        # New billitem instance
        # populate amount_due == total

        instance.amount_due = instance.total

    else:
        curr_obj = BillItem.objects.get(id=instance.id)
        if instance.total != curr_obj.total:
            instance.amount_due = instance.total


# BILL PAYMENT SIGNALS
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
            # undo the current object's payment
            billitem.amount_due += curr_obj.amount
            billitem.save()


@receiver(post_save, sender=BillPayment)
def billpayment_postsave_receiver(sender, instance, created, **kwargs):
    if created:
        # when a billpayment is created, devrease its billitem amount_due
        billitem = instance.billitem
        billitem.amount_due -= instance.amount
        billitem.save()
        # Also when a payment is made, decrease the petty cash balance
        cash_man = CashManager()
        cash_man.decrease_petty_cash_balance(instance.amount)

        # and add a withdraw transaction
        CashTransaction.objects.create(
            operation='Withdraw',
            amount=instance.amount,
            date=instance.payment_date,
            payment=instance
        )
        print("cash transaction careated")
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
        cash_man = CashManager()
        cash_man.increase_cash_balance(instance.amount)
    except:
        print("There was an error deleting a billpayyment")
