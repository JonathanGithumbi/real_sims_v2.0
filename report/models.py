from django.db import models


# Create your models here.
class Report(models.Model):
    class Meta:
        permissions = [
            ('can_view_reports', "can view reports")
        ]
