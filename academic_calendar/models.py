from django.db import models

class AcademicCalendar(models.Model):
    """The system should have only one academic calendar at any given date """
    """Usage: Used in get_term"""
    def __str__(self):
        year = self.year
        year = str(year)
        return year

    year = models.IntegerField()
    term_1_start_date = models.DateField()
    term_1_end_date = models.DateField()
    term_2_start_date = models.DateField()
    term_2_end_date = models.DateField()
    term_3_start_date = models.DateField()
    term_3_end_date = models.DateField()

    