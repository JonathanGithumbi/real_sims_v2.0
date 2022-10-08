from django.db import models

# Create your models here.

class Dashboard(models.Model):
    class Meta:
        permissions=[
            ("can_view_charts","Can view management charts")
        ]
