# Generated by Django 2.2.26 on 2023-01-19 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0030_auto_20230111_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='balance_brought_forward',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
