from django.urls import path
from . import views

urlpatterns = [

    path('report/fees_arrears/',views.fees_arrears_report, name='fees_arrears_report'),
    path('report/lunch_subscribers/',views.lunch_subscribers_report, name='lunch_subscribers_report'),
    path('report/transport_subscribers',views.transport_subscribers_report, name='transport_subscribers_report')
]

