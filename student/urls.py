from django.urls import path
from . import views

urlpatterns = [
    path('',views.students, name='students'),
    path('registration/',views.register_student, name='register_student'),
    path('profile/<int:student_id>',views.student_profile, name='student_profile'),
    path('edit/profile/<int:student_id>', views.edit_student_profile, name='edit_student_profile'),
    path('delete/student<int:id>/',views.delete_student, name='delete_student')
]
