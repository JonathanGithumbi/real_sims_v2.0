# Generated by Django 2.1.2 on 2022-07-29 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20220729_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='invoice',
        ),
    ]
