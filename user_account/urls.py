from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from django.urls import re_path as url
from .forms import AuthFormWithBootstrapSpecifics, PasswordResetFormWithBootstrapSpecifics, SetPasswordFormBS, PasswordChangeFormBS
from . import views

urlpatterns = [
    path('check-quickbooks-connection/', views.check_quickbooks_connection,
         name='check_quickbooks_connection'),
    path('account-settings/', views.account_settings,
         name='account_settings'),
    path('download-qwc/<int:id>/', views.download_qwc, name='download_qwc'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout_user'),

    # Passowrd Change lets the user to change their password by themselves
    path('password_change/', auth_views.PasswordChangeView.as_view(
        form_class=PasswordChangeFormBS, success_url="{% url 'account_settings'%}"), name='password_change'),


    # Password reset enables a user to change their password if they are locked out of their account
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordResetFormWithBootstrapSpecifics),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(form_class=SetPasswordFormBS),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
