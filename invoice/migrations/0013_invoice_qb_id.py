# Generated by Django 2.1.2 on 2022-07-27 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20220727_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='qb_id',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
