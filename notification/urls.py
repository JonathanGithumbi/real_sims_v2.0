from django.urls import path
from . import views


urlpatterns = [
    path('',views.notifications,name='notifications'),
    path('notification/<int:id>', views.notification_detail, name='notification_detail')
]
