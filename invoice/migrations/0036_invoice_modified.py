# Generated by Django 2.2.9 on 2022-11-02 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0035_auto_20221029_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]