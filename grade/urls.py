from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.GradeListView.as_view(), name='grade_list'),
    path('create/', views.GradeCreateView.as_view(), name='create_grade'),
    path('update/<int:pk>/', views.GradeUpdateView.as_view(), name="update_grade"),
    path('read/<int:pk>/', views.GradeReadView.as_view(), name="read_grade"),
    path('delete/<int:pk>/', views.GradeDeleteView.as_view(), name='delete_grade'),
    path('list/grades/', views.grades, name='grades')
]
