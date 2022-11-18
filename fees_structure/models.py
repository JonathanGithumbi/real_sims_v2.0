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
            ("can_create_a_fees_structure", "can edit the fees structure"),
            ("can_view_the_fees_structure", "can view the fees structure")

        ]
    #grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    grades = models.CharField(max_length=255, default=None)
    year = models.IntegerField(null=True)
    term = models.IntegerField(choices=TERM_CHOICES)
    # One of the sales items the school is selling
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, default=None)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=None)
    ocurrence = models.CharField(max_length=30, default=None)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    year_round = models.BooleanField(default=False)
    specific_terms = models.CharField(max_length=20, default=None)

    def __str__(self):
        return "Fees Structure for Grade: " + str(self.grade) + ' Term: '+str(self.term)+' for  Item:'+str(self.item)
