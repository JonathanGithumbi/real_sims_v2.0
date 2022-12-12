from django.urls import path
from . import views
urlpatterns = [

    path('list/<int:student_pk>/', views.PaymentListView.as_view(),
         name='payment_list'),  # Capture a single group
    path('create/<int:student_pk>/',
         views.PaymentCreateView.as_view(), name='create_payment'),
    path('update/<int:pk>/<int:student_pk>/', views.PaymentUpdateView.as_view(),
         name="update_payment"),
    path('read/<int:pk>/', views.PaymentReadView.as_view(), name="read_payment"),
    path('delete/<int:pk>/<int:student_pk>', views.PaymentDeleteView.as_view(),
         name='delete_payment'),
    path('list/payments/', views.payments, name='payments')
]
