from django.urls import path
from . import views

urlpatterns = [
    path('',views.fees_structure,name='fees_structure'),
    path('edit-fees-structure/',views.edit_fees_structure,name='edit_fees_structure')
]
