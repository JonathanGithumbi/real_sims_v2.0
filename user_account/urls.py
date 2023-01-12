from django.urls import path
from . import views
#from django.shortcuts import reverse
urlpatterns = [
    path('', views.CustomLoginView.as_view(
    ), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('change-password/', views.CustomPasswordChangeView,
         name='password_change'),
    path('change-password-done/', views.CustomPasswordChangeDoneView,
         name='password_change_done'),
    path('reset-password/', views.CustomPasswordResetView,
         name='password_reset'),
    path('reset-password-done/', views.CustomPasswordResetDoneView,
         name='password_reset_done'),
    path('reset-password-confirm/', views.CustomPasswordResetConfirmView,
         name='password_reset_confirm'),
    path('reset-password-complete/', views.CustomPasswordResetCompleteView,
         name='password_reset_complete'),
    path('account-settings', views.account_settings, name='account_settings')
]
