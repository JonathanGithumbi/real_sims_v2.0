from django.shortcuts import redirect, render
from django.urls import reverse
from user_account.views import refresh
from user_account.models import Token
from django.core.exceptions import ObjectDoesNotExist
from intuitlib.client import AuthClient
from django.conf import settings

def dashboard(request):

    return render(request, 'dashboard/dashboard.html')

