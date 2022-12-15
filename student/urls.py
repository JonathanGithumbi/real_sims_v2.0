from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='create_student'),
    path('update/<int:pk>/', views.StudentUpdateView.as_view(),
         name="update_student"),
    path('read/<int:pk>/', views.StudentReadView.as_view(), name="read_student"),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(),
         name='delete_student'),
    path('list/students/', views.students, name='students'),
    path('deactivate/student/<student.pk>',
         views.deactivate_student, name="deactivate_student")
]
