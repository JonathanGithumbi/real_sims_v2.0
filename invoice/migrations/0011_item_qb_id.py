# Generated by Django 2.1.2 on 2022-07-17 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20220712_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='qb_id',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
