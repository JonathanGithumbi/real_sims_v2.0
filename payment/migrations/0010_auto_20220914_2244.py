# Generated by Django 2.1.2 on 2022-09-14 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_payment_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='note',
            field=models.CharField(default='Single Payment', max_length=255, null=True),
        ),
    ]