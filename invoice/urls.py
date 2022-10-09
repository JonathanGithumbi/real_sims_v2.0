from nturl2path import url2pathname
from django.urls import path
from . import views

urlpatterns = [
    path('invoice detail/<int:id>', views.invoice_detail, name='invoice_detail'),
    path('print/invoice/details/<int:id>', views.print_invoice_details,
         name='print_invoice_details')
]
