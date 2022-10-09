from __future__ import absolute_import
from django.urls import reverse

from requests import HTTPError
import json

from intuitlib.client import AuthClient
from intuitlib.migration import migrate
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.core import serializers
from django.contrib import messages
from user_account.services import qbo_api_call
from user_account.models import Token

from django.contrib.auth import authenticate, login

from .backends import AuthBackend
from .forms import AuthFormWithBootstrapSpecifics
from django.contrib.auth.decorators import login_required


def oauth(request):
    auth_client = AuthClient(
        settings.CLIENT_ID,
        settings.CLIENT_SECRET,
        settings.REDIRECT_URI,
        settings.ENVIRONMENT,
    )

    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    request.session['state'] = auth_client.state_token
    return redirect(url)


def callback(request):
    auth_client = AuthClient(
        settings.CLIENT_ID,
        settings.CLIENT_SECRET,
        settings.REDIRECT_URI,
        settings.ENVIRONMENT,
        state_token=request.session.get('state', None),
    )

    state_tok = request.GET.get('state', None)
    error = request.GET.get('error', None)

    if error == 'access_denied':
        messages.add_message(request, messages.WARNING, "Access Denied")
        return redirect('disconnected_dashboard')
        # messages outside the if clause

    if state_tok is None:
        return HttpResponseBadRequest()

    if state_tok != auth_client.state_token:
        return HttpResponse('unauthorized', status=401)

    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    realm_id_token = Token.objects.create()
    realm_id_token.name = 'realm_id'
    realm_id_token.key = realm_id
    realm_id_token.save()
    request.session['realm_id'] = realm_id

    if auth_code is None:
        return HttpResponseBadRequest()

    try:
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
        access_token_obj = Token.objects.create()
        access_token_obj.name = 'access_token'
        access_token_obj.key = auth_client.access_token
        access_token_obj.save()
        request.session['access_token'] = auth_client.access_token
        refresh_token_obj = Token.objects.create()
        refresh_token_obj.name = 'refresh_token'
        refresh_token_obj.key = auth_client.refresh_token
        refresh_token_obj.save()
        request.session['refresh_token'] = auth_client.refresh_token
        id_token_obj = Token.objects.create()
        id_token_obj.name = 'id_token'
        id_token_obj.key = auth_client.id_token
        id_token_obj.save()
        request.session['id_token'] = auth_client.id_token
    except AuthClientError as e:
        # just printing status_code here but it can be used for retry workflows, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)
    except Exception as e:
        print(e)
    return redirect('connected_dashboard')


def connected(request):
    auth_client = AuthClient(
        settings.CLIENT_ID,
        settings.CLIENT_SECRET,
        settings.REDIRECT_URI,
        settings.ENVIRONMENT,
        access_token=request.session.get('access_token', None),
        refresh_token=request.session.get('refresh_token', None),
        id_token=request.session.get('id_token', None),
    )

    if auth_client.id_token is not None:
        return render(request, 'connected.html', context={'openid': True})
    else:
        return render(request, 'connected.html', context={'openid': False})


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
        realm_id=realm_id_obj.key,
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
    access_token_obj.key = auth_client.access_token
    access_token_obj.save()
    refresh_token_obj.key = auth_client.refresh_token
    refresh_token_obj.save()
    return HttpResponse('New access_token: {0}'.format(auth_client.access_token))


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


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = AuthBackend()
        user = auth_backend.authenticate(
            request, username=username, password=password)
        if user is not None:
            # try to refresh tokens purely quickbooks related
            try:
                refresh(request)
            except:
                request.session['qb_synced'] = False
            else:
                request.session['qb_synced'] = True

            finally:
                login(request, user)
                return redirect('dashboard')

        else:
            # Invalid logins
            messages.error(request, "Invalid login credentials",
                           extra_tags='alert-error')
            return redirect(login_user)
    else:
        # called with get
        form = AuthFormWithBootstrapSpecifics()
        return render(request, 'user_account/registration/login.html', {'form': form})


@login_required()
def logout_view(request):
    messages.success(request, "Logged out", extra_tags="alert-danger")
    logout(request)

    return redirect(reverse('login'))
