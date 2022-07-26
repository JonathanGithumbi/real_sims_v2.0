from django.db import models
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import settings,ENVIRONMENT_VARIABLE
from quickbooks import QuickBooks
from quickbooks.objects import Item as qb_item
from account.models import Account



class Item(models.Model):
    SERVICE = 'Service'
    NONINVENTORY = 'NonInventory'
    INVENTORY = 'Inventory'
    GROUP = 'Group'
    ITEM_TYPE_CHOICES = [
        (SERVICE, 'Service'),
        (NONINVENTORY, 'Non Inventory'),
        (INVENTORY, 'Inventory'),
        (GROUP, 'Group')
    ]

    name = models.CharField(max_length=255, null=True, default=None)
    type = models.CharField(max_length=20,choices=ITEM_TYPE_CHOICES)
    qb_id = models.CharField(max_length=255, null=True, default=None)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def create_item(self,name,type):
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

        qb_item_obj = qb_item()
        qb_item_obj.Name = name
        qb_item_obj.Type = type 

        if type == "Service":
            #Income account re required for the Service items
            #But also the Expense account ref
            COST_OF_GOODS_SOLD = 'Cost of Goods Sold'
            SALES_OF_PRODUCT_INCOME = 'Sales of Product Income'
            
            income_account = Account()
            income_account_obj = income_account.create_account(name+'income account',SALES_OF_PRODUCT_INCOME)
            income_account_obj.save()

            expense_account = Account()
            expense_account_obj = expense_account.create_account(name+'expense account',COST_OF_GOODS_SOLD)
            expense_account_obj.save()

            qb_item_obj.IncomeAccountRef = income_account_obj.to_ref()
            qb_item_obj.ExpenseAccountRef = expense_account_obj.to_ref()
            
        if type == "NonInventory":
            # only Expense account ref reuired
            COST_OF_GOODS_SOLD = 'Cost of Goods Sold'
            SALES_OF_PRODUCT_INCOME = 'Sales of Product Income'

            expense_account = Account()
            expense_account_obj = expense_account.create_account(name+'expense account',COST_OF_GOODS_SOLD)
            expense_account_obj.save()

        if type == "Inventory":
            # create Expense and Income accounts
            COST_OF_GOODS_SOLD = 'Cost of Goods Sold'
            SALES_OF_PRODUCT_INCOME = 'Sales of Product Income'
            
            income_account = Account()
            income_account_obj = income_account.create_account(name+' income account',SALES_OF_PRODUCT_INCOME)
            income_account_obj.save()

            expense_account = Account()
            expense_account_obj = expense_account.create_account(name+' expense account',COST_OF_GOODS_SOLD)
            expense_account_obj.save()

            qb_item_obj.IncomeAccountRef = income_account_obj.to_ref()
            qb_item_obj.ExpenseAccountRef = expense_account_obj.to_ref()

        saved_qb_item_obj = qb_item_obj.save(qb=client)
        return saved_qb_item_obj



    def save(self, *args, **kwargs):
        saved_qb_item_obj = self.create_item(name=self.name, type=self.type)
        self.qb_id = saved_qb_item_obj.Id
        self.synced  = True
        super().save(*args, **kwargs)
        