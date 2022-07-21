from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('',views.vendors, name='vendors'),
    path('create/',views.create_vendor,name='create_vendor')
]
