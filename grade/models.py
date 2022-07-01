from django.db import models

class Grade(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=255)
    
    