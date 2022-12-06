import datetime
from datetime import timedelta
from academic_calendar.models import Year, Term
from django.core.exceptions import ObjectDoesNotExist


class CalendarManager():
    """This manager will be in charge with syncing with the server TO keep the correct date and time """
    """Also Responsible for starting the new term protocol and the new year protocol"""
    """these protocols start the process of graduating students and invoicing them"""

    def create_year(self, create_year_form):
        year = create_year_form.save()
        return year

    def delete_year(self, year):
        year.delete()
        return True

    def create_term(self, year, create_term_form):
        term_obj = create_term_form.save(commit=False)
        term_obj.year = year
        term_obj.save()
        return term_obj

    def delete_term(self, term):
        term.delete()
        return True

    def date_range(self, start, end):
        """This method returns a list of datetime instances  of days between 'start' day and 'end' day """
        delta = end - start
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        return days

    def get_year(self, date=None):
        """Returns the current year as an year instance if no argument is passed, and returns a year instance year of the date if argument is passed"""
        if date is None:
            today = datetime.date.today()
            year_obj = Year.objects.get(year=int(today.year))
            return year_obj
        else:
            year_obj = Year.objects.get(year=date.year)
            return year_obj

    def get_term(self, date=None):
        """This method returns the term object of the current term if no arg is given, otherwise returns the term object of the date passed in"""
        """Uses date_range() to retrieve the list of days in a term"""
        if date is None:
            today = datetime.date.today()
            try:
                year = Year.objects.get(year=int(today.year))
            except ObjectDoesNotExist:
                return None
            for term in year.term_set.all():
                if today in self.date_range(term.start, term.end):
                    return term

        else:
            year = Year.objects.get(year=int(date.year))
            for term in year.term_set.all():
                if date in self.date_range(term.start, term.end):
                    return term
                else:
                    return None

    def graduate_student(self, id):
        """Graduate the student at the beginning of each term"""
        pass
