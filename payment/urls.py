from django.urls import path
from . import views
urlpatterns = [

    path('list/<int:invoice_pk>/<int:student_pk>', views.PaymentListView.as_view(),
         name='payment_list'),  # Capture a single group
    path('create/<int:invoice_pk>/<int:student_pk>',
         views.PaymentCreateView.as_view(), name='create_payment'),
    path('update/<int:pk>/<int:invoice_pk>/', views.PaymentUpdateView.as_view(),
         name="update_payment"),
    path('read/<int:pk>/', views.PaymentReadView.as_view(), name="read_payment"),
    path('delete/<int:pk>/<int:invoice_pk>', views.PaymentDeleteView.as_view(),
         name='delete_payment'),
    path('list/payments/<int:invoice_pk>', views.payments, name='payments')
]
