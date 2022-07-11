from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Token(models.Model):
    def __str__(self):
        return self.name
        
    name = models.CharField(max_length=255,default=None)
    key = models.TextField(default=None,null=True)
    