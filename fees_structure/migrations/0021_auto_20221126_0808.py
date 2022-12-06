# Generated by Django 2.2.9 on 2022-11-26 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees_structure', '0020_auto_20221126_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesstructurebatch',
            name='grades',
            field=models.ManyToManyField(to='grade.Grade'),
        ),
        migrations.AlterField(
            model_name='feesstructurebatch',
            name='period',
            field=models.CharField(choices=[('year-round', 'year-round'), ('specific-terms', 'specific-terms')], default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='feesstructurebatch',
            name='terms',
            field=models.ManyToManyField(to='academic_calendar.Term'),
        ),
    ]