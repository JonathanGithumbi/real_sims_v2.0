from django.db import models
from datetime import timedelta
import datetime
class AcademicCalendar(models.Model):
    
    """The system should have only one academic calendar at any given time"""
    """Usage: Used in get_term"""

    year = models.IntegerField()
    term_1_start_date = models.DateField()
    term_1_end_date = models.DateField()
    term_2_start_date = models.DateField()
    term_2_end_date = models.DateField()
    term_3_start_date = models.DateField()
    term_3_end_date = models.DateField()

    def __str__(self):
        year = self.year
        year = str(year)
        return year


    def date_range(self,start,end):
        """This view returns a list of datetime instances  of days between 'start' day and 'end' day """
        """It is used in get_term() to retrieve the term number """
        delta = end-start
        days = [start + timedelta(days=i) for i in range(delta.days+1)]
        return days


    def get_term(self,date=None):
        """This method returns the term number (int) given the date """
        """Uses date_range() to retrieve the list of days in a term"""
        if date is None:
            today = datetime.date.today()
            calendar = AcademicCalendar.objects.get(year=today.year)
           
            term_1_days = self.date_range(calendar.term_1_start_date,calendar.term_1_end_date)
            term_2_days = self.date_range(calendar.term_2_start_date,calendar.term_2_end_date)
            term_3_days = self.date_range(calendar.term_3_start_date,calendar.term_3_end_date)

            if today in term_1_days:
                return 1
            if today in term_2_days:
                return 2
            if today in term_3_days:
                return 3

        else:
            calendar = AcademicCalendar.objects.get(year=date.year)
           
            term_1_days = self.date_range(calendar.term_1_start_date,calendar.term_1_end_date)
            term_2_days = self.date_range(calendar.term_2_start_date,calendar.term_2_end_date)
            term_3_days = self.date_range(calendar.term_3_start_date,calendar.term_3_end_date)

            if date in term_1_days:
                return 1
            if date in term_2_days:
                return 2
            if date in term_3_days:
                return 3



            