# Generated by Django 2.2.9 on 2023-01-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees_structure', '0025_auto_20221211_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingitem',
            name='terms',
            field=models.ManyToManyField(blank=True, to='academic_calendar.TermNumbers'),
        ),
    ]