# Generated by Django 2.2.9 on 2022-11-25 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees_structure', '0015_feesstructurebatchnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='feesstructure',
            name='fee_structure_batch_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fees_structure.FeesStructureBatchNumber'),
        ),
    ]
