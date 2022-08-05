# Generated by Django 2.1.2 on 2022-07-29 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0016_auto_20220728_0900'),
        ('student', '0016_remove_student_transport_fee'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='invoice',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice'),
        ),
        migrations.AddField(
            model_name='payment',
            name='qb_id',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='payment',
            name='synced',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
