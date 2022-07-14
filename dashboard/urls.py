from django.urls import path
from . import views 

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('connected/',views.connected_dashboard, name='connected_dashboard'),
    path('disconnected/',views.disconnected_dashboard, name='disconnected_dashboard')
]
