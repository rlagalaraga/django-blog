from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.utils import timezone

from rest_framework.authtoken.models import Token
from users.manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """ Overrides Django Base User. """

    #username = None
    email = models.EmailField(max_length=500, unique=True)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='profile', default='/default/img.jpg')
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)