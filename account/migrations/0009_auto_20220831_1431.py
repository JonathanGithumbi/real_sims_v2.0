# Generated by Django 2.1.2 on 2022-08-31 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220829_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='sub_type',
            field=models.CharField(blank=True, choices=[('SalesOfProductIncome', 'Sales of Product Income'), ('CostOfLaborCos', 'Cost of Labor Cost'), ('AccountsPayable', 'Accounts Payable'), ('CostOfLabor', 'Cost of Labor(Expense)'), ('Checking', 'Checking'), ('Accounts Receivable', 'Accounts Receivable'), ('', 'eMPTY')], default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.CharField(blank=True, choices=[('Cost of Goods Sold', 'Cost of Goods Sold'), ('Income', 'Income'), ('Accounts Payable', 'Accounts Payable'), ('Expense', 'Expense'), ('Bank', 'Bank'), ('Accounts Receivable', 'Accounts Receivable')], default=None, max_length=30, null=True),
        ),
    ]
