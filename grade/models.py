from django.db import models


class Grade(models.Model):
    """the classes in a school under which to group the students"""

    def __str__(self):
        return self.title

    title = models.CharField(max_length=255)
    number = models.IntegerField(null=True, default=None)
    grade_code = models.IntegerField(null=True)
