from django.urls import path
from . import views 

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('chart1',views.chart_data,name="chart data")


]
