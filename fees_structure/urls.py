from django.urls import path
from . import views

urlpatterns = [
    path('', views.fees_structure, name='fees_structure'),
    path('create/', views.create_fees_structure, name='create_fees_structure'),


]
