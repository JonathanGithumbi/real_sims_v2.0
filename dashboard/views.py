from django.shortcuts import render
from user_account.views import refresh
from user_account.models import Token
from django.core.exceptions import ObjectDoesNotExist

def dashboard(request):
    try:
        access_token = Token.objects.get(name='access_token')
        return render(request, 'dashboard/dashboard.html',{'status':'connected'})
    except Token.DoesNotExist:
        return render(request, 'dashboard/dashboard.html',{'status':'disconnected'})