from django.db import models
from django.http import HttpResponse
from quickbooks.objects import Vendor as qb_vendor
from quickbooks.exceptions import QuickbooksException

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
