from django.urls import path
from . import views

urlpatterns = [
    path('', views.students, name='students'),
    path('register/', views.register_student, name='register_student'),
    path('profile/<int:student_id>', views.student_profile, name='student_profile'),
    path('edit/<int:id>', views.edit_student_details, name='edit_student_details'),
    path('delete/student<int:id>/', views.delete_student, name='delete_student'),
    path('inactivate/<int:id>/', views.inactivate_student,
         name='inactivate_student')
]
