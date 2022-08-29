from django.db import models
from student.models import Student
from invoice.models import Invoice
class Payment(models.Model):
    # This models is for making payments for invoices.
    amount = models.DecimalField(max_digits=8, decimal_places=2,null=True, default=None)
    date_paid = models.DateField(null=True,default=None)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True, default=None)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    synced = models.BooleanField(default=False, null=True)

    def create_payment(self):
        #This method is for saving te payment transaction to quickbooks
        pass

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # Call the "real" save() method.
