# Generated by Django 2.2.9 on 2022-12-05 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0038_remove_billitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billitem',
            name='fully_paid',
        ),
        migrations.RemoveField(
            model_name='billitem',
            name='qb_id',
        ),
        migrations.RemoveField(
            model_name='billitem',
            name='synced',
        ),
    ]
