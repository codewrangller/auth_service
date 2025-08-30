from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Model for managing system users"""
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
