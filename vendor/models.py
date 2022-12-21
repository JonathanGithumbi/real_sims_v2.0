from django.db import models
from django.shortcuts import reverse
from user_account.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField(null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor-detail', kwargs={'pk': self.pk})

    def amount_owed(self):
        """Get the total amount owed to this vendor"""
        all_bills = self.bill_set.all()
        amount_owed = 0
        for bill in all_bills:
            amount_owed += bill.get_amount_due()

        return amount_owed
