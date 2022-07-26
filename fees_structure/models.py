from django.db import models
from grade.models import Grade
from item.models import Item

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
    tuition = models.ForeignKey(Item, on_delete= models.CASCADE)
    lunch = models.ForeignKey(Item, on_delete= models.CASCADE)
    transport = models.ForeignKey(Item, on_delete= models.CASCADE)
    admission = models.ForeignKey(Item, on_delete= models.CASCADE)
    diary = models.ForeignKey(Item, on_delete= models.CASCADE)
    report_book = models.ForeignKey(Item, on_delete= models.CASCADE)
    interview = models.ForeignKey(Item, on_delete= models.CASCADE)
    computer_lessons = models.ForeignKey(Item, on_delete= models.CASCADE)
    

    def __str__(self):
        return str(self.grade)



