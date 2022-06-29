from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class AuthFormWithBootstrapSpecifics(AuthenticationForm):
    username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Username'}))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingPassword','placeholder':'Password'}))