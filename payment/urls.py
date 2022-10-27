from django.urls import path, re_path, include
from . import views

urlpatterns = [

    path('record/payment/', views.make_payment, name='create_payment'),

    path('search/payments/', views.payments, name='payments'),
    path('payment-summaries/', views.payment_summaries, name='payment_summaries'),
    path('payment-summaries/payment-trend-api',
         views.chart_data, name='chart data')
]
