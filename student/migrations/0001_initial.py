# Generated by Django 2.1.2 on 2022-06-29 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('date_of_admission', models.DateField(auto_now_add=True)),
                ('primary_contact_name', models.CharField(max_length=255)),
                ('primary_contact_phone_number', models.CharField(blank=True, max_length=255)),
                ('secondary_contact_name', models.CharField(max_length=255)),
                ('secondary_contact_phone_number', models.CharField(blank=True, max_length=255)),
                ('hot_lunch', models.BooleanField(default=False)),
                ('transport', models.BooleanField(default=False)),
                ('transport_fee', models.IntegerField(default=3000)),
                ('current_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.Grade')),
                ('grade_admitted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_admitted_to', to='grade.Grade')),
            ],
        ),
    ]
