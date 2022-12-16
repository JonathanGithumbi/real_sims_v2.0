# Generated by Django 2.2.9 on 2022-12-14 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0042_auto_20221214_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='academic_calendar.Term'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='academic_calendar.Year'),
        ),
    ]