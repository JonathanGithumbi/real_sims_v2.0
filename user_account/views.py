from __future__ import absolute_import
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .backends import AuthBackend

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'user_account/login.html'
    form_class = CustomLoginForm
    authentication_form = CustomLoginForm

    def get_default_redirect_url():
        return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    next_page = '/'


class CustomPasswordChangeView():
    pass


class CustomPasswordChangeDoneView():
    pass


class CustomPasswordResetView():
    pass


class CustomPasswordResetDoneView():
    pass


class CustomPasswordResetConfirmView():
    pass


class CustomPasswordResetCompleteView():
    pass


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
                return redirect('dashboard', permanent=True)

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


def check_quickbooks_connection(request):
    pass


def quickbooks_connection_status():
    # ...Check Status Here
    # ...
    connection_status = True
    if connection_status == True:
        return 'online'
    if connection_status == False:
        return 'offline'


def account_settings(request):
    connection_status = quickbooks_connection_status()
    password_change_form = PasswordChangeForm(user=request.user)
    return render(request, 'user_account/account_settings.html', {'password_change_form': password_change_form, 'user': request.user, 'connection_status': connection_status})


def download_qwc(request, id):
    pass
