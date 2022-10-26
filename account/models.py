from django.db import models
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings
from quickbooks import QuickBooks
from quickbooks.objects import Account as qb_acc
from quickbooks.objects.base import Ref
from .tasks import createAccount

class Currency(models.Model):
    name = models.CharField(max_length=30, null=True, default=None)
    value = models.CharField(max_length=20, null=True, default=None)

    def __str__(self):

        return self.name

    def to_ref(self):
        ref = Ref()
        ref.name = self.name
        #ref.type = self.qbo_object_name
        ref.value = self.value
        return ref


class Account(models.Model):
    """This model represents an account in the chart of accounts on the quickbooks side
        Transactions are directed to different accounts from other accounts, thus maintaining some order on the quickbooks side 
    """
    COST_OF_GOODS_SOLD = 'Cost of Goods Sold'
    SALES_OF_PRODUCT_INCOME = 'SalesOfProductIncome'
    COST_OF_LABOR_COST = "CostOfLaborCos"
    INCOME = "Income"
    ACCOUNTS_PAYABLE_TYPE = "Accounts Payable"
    ACCOUNTS_PAYABLE_SUB_TYPE = "AccountsPayable"
    EXPENSE_TYPE = "Expense"
    EXPENSE_SUB_TYPE = "CostOfLabor"
    BANK_TYPE = 'Bank'
    CHECKING_SUB_TYPE = 'Checking'
    BANK_DEFAULT_SUB_TYPE = 'Default'
    ACCOUNTS_RECEIVABLE_TYPE = 'Accounts Receivable'
    ACCOUNTS_RECEIVABLE_SUB_TYPE = 'Accounts Receivable'
    EMPTY_SUB_TYPE = ''
    ACCOUNT_TYPE_CHOICES = [
        (COST_OF_GOODS_SOLD, "Cost of Goods Sold"),
        (INCOME, "Income"),
        (ACCOUNTS_PAYABLE_TYPE, "Accounts Payable"),
        (EXPENSE_TYPE, "Expense"),
        (BANK_TYPE,'Bank'),
        (ACCOUNTS_RECEIVABLE_TYPE,'Accounts Receivable')
        



    ]
    ACCOUNT_SUB_TYPE_CHOICES = [
        (SALES_OF_PRODUCT_INCOME, "Sales of Product Income"),
        (COST_OF_LABOR_COST, "Cost of Labor Cost"),
        (ACCOUNTS_PAYABLE_SUB_TYPE, "Accounts Payable"),
        (EXPENSE_SUB_TYPE, "Cost of Labor(Expense)"),
        (CHECKING_SUB_TYPE,'Checking'),
        (ACCOUNTS_RECEIVABLE_SUB_TYPE,'Accounts Receivable'),
        (EMPTY_SUB_TYPE,'eMPTY')

    ]

    name = models.CharField(max_length=255, null=True, default=None)
    type = models.CharField(
        max_length=30, choices=ACCOUNT_TYPE_CHOICES, null=True, default=None, blank=True)
    sub_type = models.CharField(
        max_length=255, choices=ACCOUNT_SUB_TYPE_CHOICES, null=True, default=None, blank=True)
    synced = models.BooleanField(default=False, null=True)
    qb_id = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return self.name


#Quickbooks online code
    #def create_account(self):
    #    """This method actually creates the a quickboooks account and saves it to both the database and to the quickbooks account"""
    #    access_token_obj = Token.objects.get(name='access_token')
    #    refresh_token_obj = Token.objects.get(name='refresh_token')
    #    realm_id_obj = Token.objects.get(name='realm_id')
    #    # create an auth_client
    #    auth_client = AuthClient(
    #        client_id=settings.CLIENT_ID,
    #        client_secret=settings.CLIENT_SECRET,
    #        access_token=access_token_obj.key,
    #        environment=settings.ENVIRONMENT,
    #        redirect_uri=settings.REDIRECT_URI
    #    )
    #    # create a quickboooks client
    #    client = QuickBooks(
    #        auth_client=auth_client,
    #        refresh_token=refresh_token_obj.key,
    #        company_id=realm_id_obj.key
    #    )
    #    qb_acc_obj = qb_acc()
    #    qb_acc_obj.Name = self.name
    #    qb_acc_obj.AccountType = self.type
    #    qb_acc_obj.AccountSubType = self.sub_type
    #    #currencyref = Currency.objects.get(value='KES')
    #    #qb_acc_obj.CurrencyRef = currencyref.to_ref()
    #    saved_qb_acc_obj = qb_acc_obj.save(qb=client)
    #    return saved_qb_acc_obj

    def save(self, *args, **kwargs):
        
        #Queue Task 
        result = createAccount.delay(self)
        #check if request was successful
        #self.qb_id = saved_qb_acc_obj.Id
        #self.synced = True

        super().save(*args, **kwargs)
