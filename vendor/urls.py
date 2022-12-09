from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('list/', views.VendorListView.as_view(), name='vendor_list'),
    path('create/', views.VendorCreateView.as_view(), name='create_vendor'),
    path('edit-vendor/<int:id>/', views.edit_vendor, name="edit_vendor"),
    path('delete-vendor/<int:id>/', views.delete_vendor, name='delete_vendor'),
    url(r'^get-vendor-editform/$', views.get_vendor_editform,
        name='get_vendor_editform')
]
