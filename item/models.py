from django.db import models
from user_account.models import User
from django.shortcuts import reverse


class Item(models.Model):
    """These are the items being charged to the students"""
    # this item
    name = models.CharField(max_length=255, null=True, default=None)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    #created_by = models.ForeignKey(User)
    #modified_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})
