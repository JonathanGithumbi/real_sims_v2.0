from django.db import models
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from quickbooks.objects import Account as qb_acc


class Account(models.Model):
    COST_OF_GOODS_SOLD = 'Cost of Goods Sold'
    SALES_OF_PRODUCT_INCOME = 'Sales of Product Income'

    ACCOUNT_TYPE_CHOICES = [
        (COST_OF_GOODS_SOLD,"Cost of Goods Sold"),
        (SALES_OF_PRODUCT_INCOME,"Sales of Product Income")
    ]

    name = models.CharField(max_length=255,null=True,default=None)
    type = models.CharField(max_length=30, choices=ACCOUNT_TYPE_CHOICES,null=True,default=None)
    synced = models.BooleanField(default=False,null=True)
    qb_id = models.CharField(max_length=255,null=True,default=None)
    

    def __str__(self):
        return self.name

    def create_account(self,name,type):
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
        qb_acc_obj = qb_acc()
        qb_acc_obj.Name = name
        qb_acc_obj.AccountType = type
        saved_qb_acc_obj = qb_acc_obj.save(qb=client)
        return saved_qb_acc_obj

    def save(self, *args, **kwargs):
        saved_qb_acc_obj = self.create_account(name=self.name,type=self.type)
        self.qb_id = saved_qb_acc_obj.Id
        self.synced = True
        super().save(*args, **kwargs)
