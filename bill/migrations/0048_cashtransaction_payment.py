# Generated by Django 2.2.26 on 2023-01-17 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0047_auto_20230116_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashtransaction',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.BillPayment'),
        ),
    ]
