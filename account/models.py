from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name', 'last_name', 'profile_image']

    objects = UserManager()


