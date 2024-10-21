from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    app_password = models.CharField(max_length=300)


    REQUIRED_FIELDS = []


