# Generated by Django 2.2.9 on 2022-12-02 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic_calendar', '0008_auto_20221201_1725'),
        ('student', '0020_student_synced'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='term_admitted',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_calendar.Term'),
        ),
        migrations.AddField(
            model_name='student',
            name='year_admitted',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_calendar.Year'),
        ),
    ]