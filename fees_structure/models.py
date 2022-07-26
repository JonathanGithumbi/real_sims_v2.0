from django.db import models
from grade.models import Grade
from item.models import Item

TERM_CHOICES = (
            (1, "1st Term"),
            (2, "2nd Term"),
            (3, "3rd Term"),
        )

class FeesStructure(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    item = models.ForeignKey(Item, on_delete= models.CASCADE,null=True, default=None)
    amount = models.DecimalField(max_digits=8,decimal_places=2,null=True, default=None)

    def __str__(self):
        return "Grade: "+ str(self.grade) + ' Term: '+str(self.term)+' Item:'+str(self.item)



