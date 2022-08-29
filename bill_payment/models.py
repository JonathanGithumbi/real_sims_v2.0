from django.db import models
from bill.models import Bill, BillItem
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks import QuickBooks
from user_account.models import Token
from quickbooks.exceptions import QuickbooksException
from vendor.models import Vendor


# Create your models here.
class BillPayment(models.Model):
    qb_id = models.CharField(max_length=255,null=True,default=None)
    vendor = models.ForeignKey(Vendor,on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    bill = models.ForeignKey(BillItem,on_delete=models.DO_NOTHING)
    synced = models.BooleanField(null=True,default=None)

    def create_qb_bill_payment_obj(self):
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
        pass

