from django.db import models
from student.models import Student
from invoice.models import Invoice
from django.shortcuts import reverse


class Payment(models.Model):
    class Meta:
        permissions = [
            ("can_view_summaries", "can view payment summaries"),
            ("can_add_fees_payments", "Can add fees payments")
        ]

    """this model represents a payment made for an invoice"""
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=None)
    date_paid = models.DateField(auto_now_add=True, null=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, null=True, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('payment-detail', kwargs={'pk': self.pk})

# obsolete:discard when possible


class OverFlow(models.Model):
    """This method holds an account of all instances where a student may have overpayed and invoice"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
