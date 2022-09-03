from django.urls import path
from . import views

urlpatterns = [

    path('create/<int:id>/',views.make_payment,name='create_payment')

]
