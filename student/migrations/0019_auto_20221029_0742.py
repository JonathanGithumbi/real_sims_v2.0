# Generated by Django 2.2.9 on 2022-10-29 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_auto_20221027_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='qb_id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='synced',
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]