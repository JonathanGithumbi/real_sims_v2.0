# Generated by Django 2.2.9 on 2022-12-17 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0028_auto_20221214_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='lunch',
        ),
        migrations.RemoveField(
            model_name='student',
            name='transport',
        ),
    ]