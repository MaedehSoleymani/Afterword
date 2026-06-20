from django.contrib.auth.backends import BaseBackend
from .models import C_User

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = C_User.objects.get(email=email)
        except C_User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return C_User.objects.get(pk=user_id)
        except C_User.DoesNotExist:
            return None