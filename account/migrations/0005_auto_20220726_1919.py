# Generated by Django 2.1.2 on 2022-07-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220726_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.CharField(choices=[('Cost of Goods Sold', 'Cost of Goods Sold'), ('Sales of Product Income', 'SalesOfProductIncome')], default=None, max_length=30, null=True),
        ),
    ]
