from django.db import models
from grade.models import Grade
from item.models import Item
from user_account.models import User
from academic_calendar.models import Term, Year
from django.shortcuts import reverse

TERM_CHOICES = (
    (1, "1st Term"),
    (2, "2nd Term"),
    (3, "3rd Term"),
)

ocurrence_choices = [
    ('recurring', 'recurring'),
    ('one-time', 'one-time'),
    ('optional', 'optional')
]
period_choices = [
    ('year-round', 'year-round'),
    ('specific-terms', 'specific-terms')
]


class BillingItem(models.Model):
    """Billing items are items that you bill to your customers/students"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    # is being charged to these gra9des
    grades = models.ManyToManyField(Grade)
    # at this amount
    amount = models.IntegerField(null=True, default=None)
    # at this frequency
    ocurrence = models.CharField(
        max_length=30, default=None, null=True, choices=ocurrence_choices)
    # incase the occurence is recurring
    period = models.CharField(
        max_length=50, default=None, null=True, choices=period_choices, blank=True)
    # incase the it recurrs on specific terms
    terms = models.ManyToManyField(Term, blank=True)

    # incase the occurence is one time
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE, null=True, blank=True)
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name='terms', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='item_created_by', default=None, null=True, blank=True)
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # one-time charged during registration
    charge_on_registration = models.BooleanField(default=False,
                                                 blank=True)

    def __str__(self):
        return str(self.item)

    def get_absolute_url(self):
        return reverse('billingitem_detail', kwargs={'pk': self.pk})


class FeesStructureBatch(models.Model):
    """A FeeStructureBatch cannot be associated with grades before it is saved"""

    pass


class FeesStructure(models.Model):
    pass
