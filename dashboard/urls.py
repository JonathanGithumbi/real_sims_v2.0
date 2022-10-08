from django.urls import path
from . import views 

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('chart1',views.ChartData.as_view())


]
