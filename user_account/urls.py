from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import AuthFormWithBootstrapSpecifics,PasswordResetFormWithBootstrapSpecifics

urlpatterns = [
    path('',auth_views.LoginView.as_view(authentication_form=AuthFormWithBootstrapSpecifics),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(form_class=PasswordResetFormWithBootstrapSpecifics),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
]
