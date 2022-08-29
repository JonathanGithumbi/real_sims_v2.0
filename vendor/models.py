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
    given_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    synced = models.BooleanField(default=False)
    qb_id = models.CharField(max_length= 255, null=True, default= None)


    def __str__(self):
        return self.given_name + ' '+ self.middle_name + ' '+ self.last_name

    # save to qb
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        access_token_obj = Token.objects.get(name='access_token')
        refresh_token_obj = Token.objects.get(name='refresh_token')
        realm_id_obj = Token.objects.get(name='realm_id')
        #create an auth_client
        auth_client = AuthClient(
            client_id = settings.CLIENT_ID,
            client_secret = settings.CLIENT_SECRET,
            access_token = access_token_obj.key,
            environment=settings.ENVIRONMENT,
            redirect_uri = settings.REDIRECT_URI
        )
        #create a quickboooks client
        client = QuickBooks(
            auth_client = auth_client,
            refresh_token = refresh_token_obj.key,
            company_id = realm_id_obj.key
        )
        vendor = qb_vendor()
        vendor.DisplayName = self.given_name + self.middle_name + self.last_name
        vendor.save(qb=client)
        self.qb_vendor_id = vendor.Id
        self.synced = True
        super().save(*args, **kwargs)
 