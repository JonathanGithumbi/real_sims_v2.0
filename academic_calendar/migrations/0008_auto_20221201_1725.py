# Generated by Django 2.2.9 on 2022-12-01 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_calendar', '0007_auto_20221201_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='year',
            name='start',
            field=models.DateField(),
        ),
    ]
