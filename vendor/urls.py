from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('view-vendors', views.view_vendors, name='view_vendors'),
    path('new-vendor/', views.add_vendor, name='add_vendor'),
    path('edit-vendor/<int:id>/', views.edit_vendor, name="edit_vendor"),
    path('delete-vendor/<int:id>/', views.delete_vendor, name='delete_vendor'),
    url(r'^get-vendor-editform/$', views.get_vendor_editform,
        name='get_vendor_editform')
]
