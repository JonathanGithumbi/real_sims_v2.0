# Generated by Django 2.2.9 on 2022-12-14 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0027_auto_20221214_1025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='contact1_phone_number',
            new_name='contact1_number',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='secondary_contact_name',
            new_name='contact2_name',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='secondary_contact_phone_number',
            new_name='contact2_number',
        ),
    ]
