# Generated by Django 2.2.9 on 2022-12-13 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0040_auto_20221213_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitem',
            name='bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.Bill'),
        ),
    ]
