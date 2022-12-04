# Generated by Django 2.2.9 on 2022-12-03 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0025_auto_20221202_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='admission_number',
        ),
        migrations.RemoveField(
            model_name='student',
            name='admission_number_formatted',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='synced',
        ),
        migrations.AddField(
            model_name='student',
            name='visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_term', to='academic_calendar.Term'),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_year', to='academic_calendar.Year'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='lunch',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='primary_contact_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='secondary_contact_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='term_admitted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_calendar.Term'),
        ),
        migrations.AlterField(
            model_name='student',
            name='transport',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='year_admitted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_calendar.Year'),
        ),
    ]
