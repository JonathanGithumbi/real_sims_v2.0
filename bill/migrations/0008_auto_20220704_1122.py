# Generated by Django 2.1.2 on 2022-07-04 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0007_billitem_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billitem',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]