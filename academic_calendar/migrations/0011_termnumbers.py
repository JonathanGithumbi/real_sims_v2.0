# Generated by Django 2.2.9 on 2023-01-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_calendar', '0010_auto_20221206_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermNumbers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.IntegerField()),
            ],
        ),
    ]