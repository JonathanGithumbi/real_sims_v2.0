from django.urls import path
from . import views

urlpatterns = [
    path('',views.fees_structure, name='fees_structure'),
    path('update/fees_structure/<int:id>',views.update_fees_structure, name='update_fees_structure')
]
