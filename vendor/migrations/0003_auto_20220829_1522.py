# Generated by Django 2.1.2 on 2022-08-29 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_qb_vendor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='qb_vendor_id',
            new_name='qb_id',
        ),
    ]
