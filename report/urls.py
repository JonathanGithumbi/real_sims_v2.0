from django.urls import path
from . import views

urlpatterns = [
    path('',views.reports, name='reports'),
    path('report/fees_arrears/',views.generate_fees_arrears_report, name='fees_arrears_report'),
    path('report/lunch_subscribers/',views.generate_lunch_subscribers_report, name='lunch_subscribers_report'),
    path('report/transport_subscribers',views.generate_transport_subscribers_report, name='transport_subscribers_report')
]

