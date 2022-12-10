from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('list/', views.VendorListView.as_view(), name='vendor_list'),
    path('create/', views.VendorCreateView.as_view(), name='create_vendor'),
    path('update/<int:pk>/', views.VendorUpdateView.as_view(), name="update_vendor"),
    path('read/<int:pk>/', views.VendorReadView.as_view(), name="read_vendor"),
    path('delete/<int:pk>/', views.VendorDeleteView.as_view(), name='delete_vendor'),
    path('list/vendors/', views.vendors, name='vendors')
]
