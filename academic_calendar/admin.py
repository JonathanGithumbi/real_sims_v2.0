from django.contrib import admin

from academic_calendar.models import AcademicCalendar, Year, Term


admin.site.register(AcademicCalendar)
admin.site.register(Term)
admin.site.register(Year)
