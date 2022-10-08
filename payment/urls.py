from django.urls import path, re_path
from . import views

urlpatterns = [

    path('record/payment/', views.make_payment, name='create_payment'),
    path('search/payments/', views.payments, name='payments'),
    path('payment-summaries/', views.payment_summaries, name='payment_summaries'),
    re_path(r'^student-autocomplete/$',
            views.StudentAutocomplete.as_view(),
            name='student-autocomplete',),
    path('payment-summaries/payment-trend-api',
         views.PaymentTrendChart.as_view())
]
