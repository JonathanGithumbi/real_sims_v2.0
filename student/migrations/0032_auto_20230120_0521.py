# Generated by Django 2.2.26 on 2023-01-20 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic_calendar', '0012_auto_20230102_1222'),
        ('student', '0031_student_balance_brought_forward'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='onboarding_term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='onboarding_term', to='academic_calendar.Term'),
        ),
        migrations.AddField(
            model_name='student',
            name='onboarding_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='onboarding_year', to='academic_calendar.Year'),
        ),
    ]