from django.urls import path
from . import views

urlpatterns = [
    path('<int:student_ids>/',views.payments, name='payments'),
    path('create/',views.create_payment,name='create_payment')

]
