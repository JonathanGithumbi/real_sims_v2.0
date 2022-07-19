from django.db import models

class Payment(models.Model):
    pass
    def save(self, *args, **kwargs):
        #create payment
        super().save(*args, **kwargs)