from django.db import models
from grade.models import Grade
TERM_CHOICES = (
            (1, "1st Term"),
            (2, "2nd Term"),
            (3, "3rd Term"),
        )
YEAR_CHOICES = ((0, "..."),
            (2020, "2020"),
            (2021, "2021"),
            (2022, "2022"),
            (1, "..."))

class FeesStructure(models.Model):
    
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    tuition = models.IntegerField()
    lunch = models.IntegerField()
    transport = models.IntegerField()
    admission = models.IntegerField()
    diary = models.IntegerField(null=True,default=None)
    report_book = models.IntegerField(null=True,default=None)
    interview = models.IntegerField()
    computer_lessons = models.IntegerField()
    #Include transport 

    def __str__(self):
        return str(self.grade)



