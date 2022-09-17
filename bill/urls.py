from django.urls import path
from . import views

urlpatterns = [
    path('',views.bills, name='bills'),
    path('create/', views.create_bill, name='create_bill'),
    path('pay/bill/<int:id>',views.pay_bill, name='pay_bill'),
    path('edit/<int:id>/',views.edit_bill,name='edit_bill')
    
]
