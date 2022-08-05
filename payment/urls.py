from django.urls import path
from . import views

urlpatterns = [

    path('create/<int:id>/',views.create_payment,name='create_payment')

]
