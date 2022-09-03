from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class AuthFormWithBootstrapSpecifics(AuthenticationForm):
    #the school's email
    username = forms.CharField(max_length=254,widget=forms.EmailInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Username'}))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingPassword','placeholder':'Password'}))


class PasswordResetFormWithBootstrapSpecifics(PasswordResetForm):
    email=forms.EmailField(label=_("Email"), max_length=254,widget=forms.EmailInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Email'}))
