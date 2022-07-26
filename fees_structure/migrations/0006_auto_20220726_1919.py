# Generated by Django 2.1.2 on 2022-07-26 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('fees_structure', '0005_auto_20220726_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feesstructure',
            name='admission',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='computer_lessons',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='diary',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='interview',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='lunch',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='report_book',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='transport',
        ),
        migrations.RemoveField(
            model_name='feesstructure',
            name='tuition',
        ),
        migrations.AddField(
            model_name='feesstructure',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='feesstructure',
            name='item',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item'),
        ),
    ]