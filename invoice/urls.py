from django.urls import path
from . import views
urlpatterns = [
    path('list/<int:invoice_pk>/', views.InvoiceItemListView.as_view(),
         name='invoiceitem_list'),  # Capture a single group
    path('create/<int:invoice_pk>/',
         views.InvoiceItemCreateView.as_view(), name='create_invoiceitem'),
    path('update/<int:pk>/<int:invoice_pk>/', views.InvoiceItemUpdateView.as_view(),
         name="update_invoiceitem"),
    path('read/<int:pk>/', views.InvoiceItemReadView.as_view(), name="read_invoiceitem"),
    path('delete/<int:pk>/<int:invoice_pk>', views.InvoiceItemDeleteView.as_view(),
         name='delete_invoiceitem'),
    path('list/invoiceitems/', views.invoiceitems, name='invoiceitems'),
    path('list/<int:student_pk>/', views.InvoiceListView.as_view(),
         name='invoice_list'),  # Capture a single group
    path('create/<int:student_pk>/',
         views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('update/<int:pk>/<int:student_pk>/', views.InvoiceUpdateView.as_view(),
         name="update_invoice"),
    path('read/<int:pk>/', views.InvoiceReadView.as_view(), name="read_invoice"),
    path('delete/<int:pk>/<int:student_pk>', views.InvoiceDeleteView.as_view(),
         name='delete_invoice'),
    path('list/invoices/', views.invoices, name='invoices'),
    
]
