from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from .forms import AuthFormWithBootstrapSpecifics,PasswordResetFormWithBootstrapSpecifics
from . import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(authentication_form=AuthFormWithBootstrapSpecifics),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(form_class=PasswordResetFormWithBootstrapSpecifics),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    #url(r'^$', views.index, name='index'),
    url(r'^oauth/?$', views.oauth, name='oauth'),
    url(r'^callback/?$', views.callback, name='callback'),
    url(r'^connected/?$', views.connected, name='connected'),
    url(r'^qbo_request/?$', views.qbo_request, name='qbo_request'),
    url(r'^revoke/?$', views.revoke, name='revoke'),
    url(r'^refresh/?$', views.refresh, name='refresh'),
    url(r'^user_info/?$', views.user_info, name='user_info'),

]



