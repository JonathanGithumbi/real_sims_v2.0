# Generated by Django 2.2.9 on 2022-12-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_auto_20221202_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_of_admission',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]