from django.db import models
from django.shortcuts import reverse
from user_account.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor-detail', kwargs={'pk': self.pk})
