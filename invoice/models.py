
from django.db import models

from grade.models import Grade


from item.models import Item as sales_item

from academic_calendar.models import Year, Term
from student.models import Student


class Invoice(models.Model):
    """An Invoice. Charged to the active students at the beginning of every term."""
    class Meta:
        db_table = "Invoice_invoice"

    balance = models.IntegerField(null=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING, null=True)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, null=True, default=None)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def status(self):
        if self.balance is None:
            return 'Not Fully Paid'
        if self.balance == 0:
            return 'Fully Paid'
        if self.balance < 0:
            return 'Overpaid'
        if self.balance > 0:
            return 'Not Fully Paid'

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
            amount = amount+item.amount

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


class Item(models.Model):
    """These are invoice items. i.e the items that compose the invoice"""
    """Whenever an invoice item is added to an invoice, the save method modifies the invoice by increasing the amount and balance of the invoice"""
    # item_description = models.CharField(max_length=255,null=True,default=None)
    sales_item = models.ForeignKey(
        sales_item, on_delete=models.DO_NOTHING, null=True, default=None)
    amount = models.IntegerField(null=True, default=None)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.invoice_item.name


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
