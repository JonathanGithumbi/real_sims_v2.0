from django.db import models
from datetime import timedelta
import datetime
from django.core.exceptions import ObjectDoesNotExist


class AcademicCalendar(models.Model):
    """This Class contains the start and end date for each term of a given year
    The system uses it so that it can find out what term to charge the student for.So it is a very critical part of the system
    """

    year = models.IntegerField(unique=True)
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

    def date_range(self, start, end):
        """This view returns a list of datetime instances  of days between 'start' day and 'end' day """
        delta = end - start
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        return days

    def get_year(self, date=None):
        """Returns the current year as an integer if no argument is passed, and returns the integer year of the date if argument is passed"""
        if date is None:
            today = datetime.date.today()
            return int(today.year)

        else:
            return int(date.year)

    def get_term(self, date=None):
        """This method returns the term number of the current term if no arg is given, otherwise returns the term number of the date passed in"""
        """Uses date_range() to retrieve the list of days in a term"""
        if date is None:
            today = datetime.date.today()
            try:
                calendar = AcademicCalendar.objects.get(year=today.year)
            except ObjectDoesNotExist:
                return None

            term_1_days = self.date_range(
                calendar.term_1_start_date, calendar.term_1_end_date)
            term_2_days = self.date_range(
                calendar.term_2_start_date, calendar.term_2_end_date)
            term_3_days = self.date_range(
                calendar.term_3_start_date, calendar.term_3_end_date)

            if today in term_1_days:
                return 1
            if today in term_2_days:
                return 2
            if today in term_3_days:
                return 3

        else:
            calendar = AcademicCalendar.objects.get(year=date.year)

            term_1_days = self.date_range(
                calendar.term_1_start_date, calendar.term_1_end_date)
            term_2_days = self.date_range(
                calendar.term_2_start_date, calendar.term_2_end_date)
            term_3_days = self.date_range(
                calendar.term_3_start_date, calendar.term_3_end_date)

            if date in term_1_days:
                return 1
            if date in term_2_days:
                return 2
            if date in term_3_days:
                return 3

    def term_begun(self, date):
        """This function is used to check whether the date given falls within any term"""
        cal = AcademicCalendar.objects.get(year=date.year)
        if cal is not None:
            term_1_days = self.date_range(
                cal.term_1_start_date, cal.term_1_end_date)
            term_2_days = self.date_range(
                cal.term_2_start_date, cal.term_2_end_date)
            term_3_days = self.date_range(
                cal.term_3_start_date, cal.term_3_end_date)

            if date in term_1_days:
                return True
            if date in term_2_days:
                return True
            if date in term_3_days:
                return True
            else:
                return False
        else:
            raise Exception("Not Available")
