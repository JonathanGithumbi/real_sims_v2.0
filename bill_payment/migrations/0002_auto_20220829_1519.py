# Generated by Django 2.1.2 on 2022-08-29 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill_payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billpayment',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bill.BillItem'),
        ),
        migrations.AlterField(
            model_name='billpayment',
            name='qb_id',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]