# Generated by Django 4.1.2 on 2022-10-23 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='amount',
        ),
    ]
