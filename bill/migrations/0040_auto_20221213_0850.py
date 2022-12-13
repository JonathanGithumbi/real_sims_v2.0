# Generated by Django 2.2.9 on 2022-12-13 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_vendor_phone_number'),
        ('bill', '0039_auto_20221205_0756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billitem',
            options={},
        ),
        migrations.RemoveField(
            model_name='bill',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='bill_number',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='synced',
        ),
        migrations.RemoveField(
            model_name='billitem',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='billitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='billitem',
            name='recipient',
        ),
        migrations.AddField(
            model_name='bill',
            name='billing_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='payment_status',
            field=models.CharField(choices=[('Fully Paid', 'Fully Paid'), ('Partly Paid', 'Partly Paid'), ('Unpaid', 'Unpaid')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vendor.Vendor'),
        ),
    ]
