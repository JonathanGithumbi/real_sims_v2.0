"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url

from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView

#from QBWEBSERVICE.views import qb_web_service, app, QBWEBSERVICE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_account.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('student/', include('student.urls')),
    path('bill/', include('bill.urls')),
    path('reports/', include('report.urls')),
    path('user_account/', include('user_account.urls')),
    path('invoice/', include('invoice.urls')),
    path('payments/', include('payment.urls')),
    path('fees-structure/', include('fees_structure.urls')),
    path('expenses/', include('expenses.urls')),
    path('qwc/', include('QBWEBSERVICE.urls'))
]
