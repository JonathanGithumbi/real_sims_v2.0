from django.urls import path
from . import views

urlpatterns = [

    path('record/payment/',views.make_payment,name='create_payment'),
    path('search/payments/',views.payments,name='payments')

]
