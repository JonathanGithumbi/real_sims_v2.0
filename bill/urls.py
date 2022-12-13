from django.urls import path
from . import views
urlpatterns = [
    # Bill items urls
    path('list/bill-item/<int:bill_pk>/', views.BillItemListView.as_view(),
         name='billitem_list'),  # Capture a single group
    path('create/bill-item/<int:bill_pk>/',
         views.BillItemCreateView.as_view(), name='create_billitem'),
    path('update/bill-item/<int:pk>/<int:bill_pk>/', views.BillItemUpdateView.as_view(),
         name="update_billitem"),
    path('read/bill-item/<int:pk>/', views.BillItemReadView.as_view(),
         name="read_billitem"),
    path('delete/bill-item/<int:pk>/<int:bill_pk>', views.BillItemDeleteView.as_view(),
         name='delete_billitem'),
    path('list/billitems/<int:bill_pk>', views.billitems, name='billitems'),

    # Bill Urls

    path('list/', views.BillListView.as_view(),
         name='bill_list'),  # Capture a single group
    path('create/',
         views.BillCreateView.as_view(), name='create_bill'),
    path('update/<int:pk>/', views.BillUpdateView.as_view(),
         name="update_bill"),
    path('read/<int:pk>/', views.BillReadView.as_view(), name="read_bill"),
    path('delete/<int:pk>/', views.BillDeleteView.as_view(),
         name='delete_bill'),
    path('list/bills/', views.bills, name='bills'),

]
