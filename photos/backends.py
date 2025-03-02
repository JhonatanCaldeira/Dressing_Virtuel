from django.contrib.auth.backends import BaseBackend
from .models import ClientProfile

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = ClientProfile.objects.get(email=email)
            #print(user)
            #print(user.check_password(password))
            if user.check_password(password):
                return user
        except ClientProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ClientProfile.objects.get(pk=user_id)
        except ClientProfile.DoesNotExist:
            return None
