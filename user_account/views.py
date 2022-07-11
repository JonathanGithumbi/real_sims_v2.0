from __future__ import absolute_import
from django.urls import reverse

from requests import HTTPError
import json

from intuitlib.client import AuthClient
from intuitlib.migration import migrate
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.core import serializers
from django.contrib import messages
from user_account.services import qbo_api_call
from user_account.models import Token

# Create your views here.
def oauth(request):
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT,
    )

    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    #request.session['state'] = auth_client.state_token
    try:
        state = Token.objects.get(name='state')
    except Token.DoesNotExist:
        state = Token.objects.create(name='state')
        
    state.key = auth_client.state_token
    state.save()
    return redirect(url)

def openid(request):
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT,
    )

    url = auth_client.get_authorization_url([Scopes.OPENID, Scopes.EMAIL])
    request.session['state'] = auth_client.state_token
    return redirect(url)

def callback(request):
    state = Token.objects.get(name='state')
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        state_token=state.key
        #state_token=request.session.get('state', None),
    )

    state_tok = request.GET.get('state', None)
    error = request.GET.get('error', None)
    
    if error == 'access_denied':
        return redirect(reverse('dashboard'))
    messages.error(request,"Access to quickbooks account denied")#messages outside the if clause
    
    if state_tok is None:
        return redirect(reverse('dashboard'))
    messages.error(request,"State_tok is None")

    if state_tok != auth_client.state_token:  
        return redirect(reverse('dashboard'))
    messages.error(request,"Unauthorized")
    
    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    try:
        realm_id_obj = Token.objects.get(name='realm_id')
    except Token.DoesNotExist:
        realm_id_obj = Token.objects.create(name='realm_id')

    realm_id_obj.key = realm_id
    realm_id_obj.save()
    #request.session['realm_id'] = realm_id


    if auth_code is None:
        messages.add_message(request,messages.ERROR,"Error: Auth Code is None")
        return redirect(reverse('no_auth_code'))
    messages.error(request,"Auth code is none")

    try:
        auth_client.get_bearer_token(auth_code, realm_id=realm_id_obj.key)
        #request.session['access_token'] = auth_client.access_token
        try:
            access_token_obj = Token.objects.get('access_token')
        except Token.DoesNotExist:
            access_token_obj = Token.objects.create(name='access_token')

        access_token_obj.key = auth_client.access_token
        access_token_obj.save()
        #request.session['refresh_token'] = auth_client.refresh_token
        try:
            refresh_token_obj = Token.objects.get('refresh_token')
        except Token.DoesNotExist:
            refresh_token_obj.objects.create(name='refresh_token')
        refresh_token_obj.key = auth_client.refresh_token
        refresh_token_obj.save()
        #request.session['id_token'] = auth_client.id_token
        try:
            id_token_obj = Token.objects.get('id_token')
        except Token.DoesNotExist:
            id_token_obj.objects.create(name='id_token')

        id_token_obj.key = auth_client.id_token
        id_token_obj.save()
    except AuthClientError as e:
        # just printing status_code here but it can be used for retry workflows, etc
        return redirect(reverse('dashboard'))

        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)
    
    except Exception as e:
        print(e)
        messages.add_message(request,messages.ERROR,"Exceptio as e")
        return redirect(reverse('dashboard'))
    messages.error(request, "AuthCLient error exception")

    return redirect(reverse('connected'))
    

def connected(request):
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    id_token_obj = Token.objects.get(name='id_token')
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        #access_token=request.session.get('access_token', None), 
        access_token = access_token_obj.key,
        #refresh_token=request.session.get('refresh_token', None),
        refresh_token = refresh_token_obj.key,
        #id_token=request.session.get('id_token', None),
        id_token = id_token_obj.key
    )

    if auth_client.id_token is not None:
        messages.add_message(request,messages.SUCCESS,"auth client id_token is not none")
        return redirect(reverse('dashboard'))
    else:
        messages.add_message(request,messages.ERROR,"auth client id_token is none")
        return redirect(reverse('dashboard'))

def qbo_request(request):
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    realm_id_obj = Token.objects.get(name='realm_id')
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=access_token_obj.key, 
        refresh_token=refresh_token_obj.key, 
        realm_id = realm_id_obj.key,
    )

    if auth_client.access_token is not None:
        access_token = auth_client.access_token

    if auth_client.realm_id is None:
        raise ValueError('Realm id not specified.')
    response = qbo_api_call(auth_client.access_token, auth_client.realm_id)
    
    if not response.ok:
        return HttpResponse(' '.join([response.content, str(response.status_code)]))
    else:
        return HttpResponse(response.content)

def user_info(request):
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=request.session.get('access_token', None), 
        refresh_token=request.session.get('refresh_token', None), 
        id_token=request.session.get('id_token', None),
    )

    try:
        response = auth_client.get_user_info()
    except ValueError:
        return HttpResponse('id_token or access_token not found.')
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse(response.content)
        
def refresh(request):
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=access_token_obj.key, 
        refresh_token=refresh_token_obj.key, 
    )

    try:
        auth_client.refresh() 
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse('New refresh_token: {0}'.format(auth_client.refresh_token))

def revoke(request):
    access_token_obj = Token.objects.get(name='access_token')
    refresh_token_obj = Token.objects.get(name='refresh_token')
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT, 
        access_token=access_token_obj.key, 
        refresh_token=refresh_token_obj.key, 
    )
    try:
        is_revoked = auth_client.revoke()
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse('Revoke successful')


def migration(request):
    auth_client = AuthClient(
        settings.CLIENT_ID, 
        settings.CLIENT_SECRET, 
        settings.REDIRECT_URI, 
        settings.ENVIRONMENT,
    )
    try:
        migrate(
            settings.CONSUMER_KEY, 
            settings.CONSUMER_SECRET, 
            settings.ACCESS_KEY, 
            settings.ACCESS_SECRET, 
            auth_client, 
            [Scopes.ACCOUNTING]
        )
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse('OAuth2 refresh_token {0}'.format(auth_client.refresh_token))

def no_auth_code(request):
    return render(request,'user_ccount/no_auth.html')