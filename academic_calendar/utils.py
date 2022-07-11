from academic_calendar.models import AcademicCalendar
from datetime import timedelta

def date_range(start,end):
    """This view returns a list of datetime instances  of days between 'start' day and 'end' day """
    """It is used in get_term() to retrieve the term number """
    delta = end-start
    days = [start + timedelta(days=i) for i in range(delta.days+1)]
    return days

def get_term(date):
    """This method returns the term number (int) given the date """
    """Uses date_range() to retrieve the list of days in a term"""
    """It works as long as the time on the datetime instances of AcademicCaalendar are set to 00:00 (midnight)"""
    calendar = AcademicCalendar.objects.get(year=date.year)
    term_1_start_date = calendar.term_1_start_date
    term_1_end_date = calendar.term_1_end_date
    term_2_start_date =calendar.term_2_start_date
    term_2_end_date = calendar.term_2_end_date
    term_3_start_date = calendar.term_3_start_date
    term_3_end_date = calendar.term_3_end_date

    term_1_days = date_range(term_1_start_date,term_1_end_date)
    term_2_days = date_range(term_2_start_date,term_2_end_date)
    term_3_days = date_range(term_3_start_date,term_3_end_date)

    if date in term_1_days:
        return 1
    if date in term_2_days:
        return 2
    if date in term_3_days:
        return 3
