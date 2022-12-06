# Generated by Django 2.2.9 on 2022-11-29 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_calendar', '0003_term_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='year',
        ),
        migrations.AddField(
            model_name='year',
            name='terms',
            field=models.ManyToManyField(to='academic_calendar.Term'),
        ),
    ]