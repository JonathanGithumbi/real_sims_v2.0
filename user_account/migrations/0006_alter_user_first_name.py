# Generated by Django 4.1.1 on 2022-10-01 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0005_auto_20220709_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
