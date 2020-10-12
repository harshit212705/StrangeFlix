# importing django modules
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# model for storing the basic details of all types of users
# account can be of three types--user, provider, admin
class CustomUser(AbstractUser):

    USER_TYPES = (

        # TYPES OF USERS
        ('A', 'Admin'),
        ('P', 'Provider'),
        ('U', 'User'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPES, default=USER_TYPES[2][1])


# model for storing user specific details
class UserDetails(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    wallet_money = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User Details"
