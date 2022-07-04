from django.urls import path
from . import views

urlpatterns = [
    path('',views.bills, name='bills'),
    path('create/', views.create_bill, name='create_bill')
]
