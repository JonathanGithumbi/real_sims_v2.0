
from django.db import models

from grade.models import Grade
from academic_calendar.models import Year, Term
from student.models import Student
from fees_structure.models import BillingItem
from django_quickbooks.models import QBDModelMixin

class Invoice(QBDModelMixin):
    """An Invoice. Charged to the active students at the beginning of every term."""
    class Meta:
        db_table = "Invoice_invoice"
        get_latest_by = 'created_sys'

    balance = models.IntegerField(default=0)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING, null=True)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, null=True, default=None)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_sys = models.DateTimeField(auto_now_add=True, null=True)

    def to_qbd_obj(self,**fields):
        pass

    @classmethod
    def from_qbd_obj(cls,qbd_obj):
        pass
    
    def status(self):
        if self.balance == self.get_total_amount():
            return 'unpaid'
        if self.balance == 0:
            return 'paid'
        if self.balance < self.get_total_amount():
            return 'partially-paid'

    def fully_paid(self):
        balance = self.get_balance()
        if balance != 0:
            return False
        if balance == 0:
            return True

    def get_term(self):
        return self.term

    def get_year(self):
        return self.year

    def get_total_amount(self):
        amount = 0
        items = Item.objects.filter(invoice=self)
        for item in items:
            amount = amount+item.billing_item.amount

        return amount

    def get_amount_paid(self):
        payments = self.payment_set.filter(invoice=self)
        payment_amount = 0
        for payment in payments:
            payment_amount = payment_amount + payment.amount

        return payment_amount

    def get_balance(self):
        # amount-payment amount
        if self.balance is None:
            return self.get_total_amount()
        else:
            return self.balance


class Item(models.Model):  # in instance of this model is a sale of a billing item against an invoice
    """These are invoice items. i.e the items that compose the invoice"""
    """Whenever an invoice item is added to an invoice, the save method modifies the invoice by increasing the amount and balance of the invoice"""
    # item_description = models.CharField(max_length=255,null=True,default=None)
    billing_item = models.ForeignKey(
        BillingItem, on_delete=models.CASCADE, related_name="sales_item", null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.billing_item.item.name


class BalanceTable(models.Model):
    """This table reflects the accumulation of all of a students amount owed to the school
    this table is updated whenever a payment is made and whenever an invoice is created
    this table should not allow deletion of a student if they;re balance is not 0
    wheneve the invoice is added, the amoun is added to the balance 
    whenever a payment is made, the amount is deducted from the balance 
    Negative numbers mean that the student owes the school while positive numbers means that the school owes the student
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    modified = models.DateTimeField(auto_now=True)

    def increase_balance(self, amount):
        self.balance = self.balance + amount
        self.save()

    def decrease_balance(self, amount):
        self.balance = self.balance - amount
        self.save()

    def get_balance(self):
        return self.balance


# Obsolete Delete when possible
class InvoiceNumber(models.Model):
    """Generates the invoice number from instance's id attribute """
    """should it be linked to qb_invoice invoice number."""
    created = models.DateTimeField(auto_now_add=True)
