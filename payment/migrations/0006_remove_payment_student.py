# Generated by Django 2.1.2 on 2022-08-31 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_payment_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='student',
        ),
    ]
