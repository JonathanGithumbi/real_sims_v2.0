from django.urls import path
from . import views

urlpatterns = [
    path('',views.academic_calendar,name='academic_calendar'),
    path('create/academic_calendar/',views.create_academic_calendar, name='create_academic_calendar'),
    path('update/academic_calendar/<int:id>',views.update_academic_calendar, name='update_academic_calendar'),
    path('delete/academic_calendar/<int:id>',views.delete_academic_calendar,name='delete_academic_calendar')
]
