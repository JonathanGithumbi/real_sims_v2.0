# Generated by Django 2.1.2 on 2022-07-12 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_auto_20220711_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-created']},
        ),
    ]
