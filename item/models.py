from django.db import models
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import settings, ENVIRONMENT_VARIABLE
from quickbooks import QuickBooks
from quickbooks.objects import Item as qb_item
from account.models import Account


class Item(models.Model):
    """These are the items being charged to the students"""
    # this item
    name = models.CharField(max_length=255, null=True, default=None)


    def __str__(self):
        return self.name
