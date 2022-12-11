from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.BillingItemListView.as_view(), name='billingitem_list'),
    path('create/', views.BillingItemCreateView.as_view(), name='create_billingitem'),
    path('update/<int:pk>/', views.BillingItemUpdateView.as_view(), name="update_billingitem"),
    path('read/<int:pk>/', views.BillingItemReadView.as_view(), name="read_billingitem"),
    path('delete/<int:pk>/', views.BillingItemDeleteView.as_view(), name='delete_billingitem'),
    path('list/billingitems/', views.billingitems, name='billingitems')
]
