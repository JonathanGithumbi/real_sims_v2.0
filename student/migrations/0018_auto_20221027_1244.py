# Generated by Django 2.2.9 on 2022-10-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_student_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='qbd_object_id',
            field=models.CharField(editable=False, max_length=127, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='qbd_object_updated_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='qbd_object_version',
            field=models.CharField(editable=False, max_length=127, null=True),
        ),
    ]