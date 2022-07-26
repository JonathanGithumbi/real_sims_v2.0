from django.shortcuts import redirect, render
from django.urls import reverse
from user_account.views import refresh
from user_account.models import Token
from django.core.exceptions import ObjectDoesNotExist
from intuitlib.client import AuthClient
from django.conf import settings

def dashboard(request):
    """Check Whether You are connected and redirect accordingly"""
    """Check if i have the access tokenin db"""
    access_token_obj = Token.objects.get(name='access_token')
    if access_token_obj is not None:
        return redirect('connected_dashboard')
    else:
        return redirect(reverse('disconnected_dashboard'))

def connected_dashboard(request):
    """Check whether you're app is connected if not redirect to disconnected app"""
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    id_token_obj = Token.objects.get(name='id_token')

    """auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=access_token_obj.key,
        refresh_token=refresh_token_obj.key,
        id_token=id_token_obj.key
    )"""

    return render(request, 'dashboard/connected_dashboard.html')

def disconnected_dashboard(request):
    """Check whether you are connected, if so redirect to connected"""
    return render(request,'dashboard/disconnected_dashboard.html')

