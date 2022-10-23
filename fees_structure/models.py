from django.db import models
from grade.models import Grade
from item.models import Item

TERM_CHOICES = (
            (1, "1st Term"),
            (2, "2nd Term"),
            (3, "3rd Term"),
        )

class FeesStructure(models.Model):
    class Meta:
        permissions = [
            ("can_edit_the_fees_structure", "can edit the fees structure"),
            ("can_view_the_fees_structure", "can view the fees structure")
            
        ]
    """this model composes the entire school fees structure,"""
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    item = models.ForeignKey(Item, on_delete= models.CASCADE,null=True, default=None)#One of the sales items the school is selling
    amount = models.DecimalField(max_digits=8,decimal_places=2,null=True, default=None)

    def __str__(self):
        return "Fees Structure for Grade: "+ str(self.grade) + ' Term: '+str(self.term)+' for  Item:'+str(self.item)



