from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_fees_structure, name='create_fees_structure'),
    path('view/', views.view_fees_structure, name='view_fees_structure'),
    path('edit/<int:id>', views.edit_fees_structure, name='edit_fees_structure'),
    path('delete/<int:id>/', views.delete_fees_structure,
         name='delete_fees_structure')
]
