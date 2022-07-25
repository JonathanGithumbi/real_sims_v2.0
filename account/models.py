from django.db import models
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from quickbooks.objects import Account as qb_acc


class Account(models.Model):
    qb_acc_id = models.CharField(max_length=255,null=True,default=None)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
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

        #create an Account
        qb_acc_obj = qb_acc()
        qb_acc_obj.Name = self.name
        qb_acc_obj.AccountSubType = "OtherMiscellaneousServiceCost"
        acc_obj = qb_acc_obj.save(qb=client)
        self.qb_acc_id = acc_obj.Id
        super().save(*args, **kwargs)
