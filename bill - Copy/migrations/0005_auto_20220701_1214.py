# Generated by Django 2.1.2 on 2022-07-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0004_auto_20220701_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=7, null=True),
        ),
    ]