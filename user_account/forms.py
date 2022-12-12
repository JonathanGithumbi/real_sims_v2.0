from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.core import validators


class CustomLoginForm(AuthenticationForm):
    # the school's email
    username = forms.CharField(max_length=254, required=True, validators=[validators.validate_email], widget=forms.EmailInput(
        attrs={'class': 'form-control  form-control-sm', 'id': 'floatingInput', 'autocomplete': "autocomplete", 'autofocus': True}))
    password = forms.CharField(label=_("Password"), required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'floatingPassword', 'autocomplete': 'off'}))


class PasswordResetFormWithBootstrapSpecifics(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), required=True, validators=[validators.validate_email], max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}))


class SetPasswordFormBS(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'autocomplete': 'off'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'autocomplete': 'off'}),
    )


class PasswordChangeFormBS(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',
                                   'id': 'floatingInput', 'autocomplete': False, 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'autocomplete': 'off'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput', 'autocomplete': 'off'}),
    )
