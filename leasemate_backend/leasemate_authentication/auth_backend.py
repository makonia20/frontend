from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = UserModel.objects.get(username=username)  # Check for username only
        except UserModel.DoesNotExist:
            return None  # Return None if user is not found

        if user and user.check_password(password):
            return user
        return None  # Return None if password is incorrect

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
