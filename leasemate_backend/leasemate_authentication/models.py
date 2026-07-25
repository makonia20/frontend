from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class LeasemateUserManager(BaseUserManager):
    def create_user(self, username, phone, id_number, first_name, last_name, password=None, middle_name=None):
        if not username:
            raise ValueError("Users must have a username")
        if not phone:
            raise ValueError("Users must have a phone number")
        if not id_number:
            raise ValueError("Users must have an ID number")
        if not first_name or not last_name:
            raise ValueError("Users must provide full name")

        user = self.model(
            username=username,  # Include username
            phone=phone,
            id_number=id_number,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class LeasemateUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)  # New username field
    phone = models.CharField(max_length=10, unique=True)
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)

    objects = LeasemateUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'id_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.contrib.auth.backends import ModelBackend
from .models import LeasemateUser

class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = LeasemateUser.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except LeasemateUser.DoesNotExist:
            return None
