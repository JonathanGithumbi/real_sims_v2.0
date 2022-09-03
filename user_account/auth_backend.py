from django.contrib.auth import backends
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend

class AuthBackend(backends.BaseBackend):
    """My custom backend which will fetch a new token key """
    def get_user(self, user_id):
        #user_id can be anything as long as that thing is the primary key of your user object
        #returns a user_object or None
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self,request,username = None, password=None):
        #checks the credentials an returns a user if credentials valid otherwise returns None

        #check if that user exists
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        #check if the password is correct
        if check_password(password,user.password):
            return user
        else:
            return None
        
