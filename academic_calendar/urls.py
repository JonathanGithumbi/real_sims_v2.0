from django.urls import path
from . import views
urlpatterns = [
    path('calendars/', views.academic_calendars, name='academic_calendars'),
    path('calendar/<int:id>', views.academic_calendar, name='academic_calendar'),
    path('term/edit/<int:id>', views.edit_term, name='edit_term'),
    path('term/delete/<int:id>', views.delete_term, name='delete_term'),
    path('discard/<int:id>', views.delete_year, name='delete_year'),
    path('create/', views.create_year, name="create_year"),
    path('create/term/', views.create_term, name="create_term"),

]
