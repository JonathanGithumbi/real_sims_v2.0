# Generated by Django 4.1.1 on 2022-10-18 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0031_alter_billitem_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitem',
            name='petty_cash_balance',
            field=models.IntegerField(null=True),
        ),
    ]
