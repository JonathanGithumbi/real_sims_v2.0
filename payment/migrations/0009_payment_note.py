# Generated by Django 2.1.2 on 2022-09-14 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_payment_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='note',
            field=models.CharField(default=True, max_length=255, null=True),
        ),
    ]