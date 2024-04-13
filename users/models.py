from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Define gender choices
genders = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Define gender choices
genders = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField(default=0)
    user_type = models.CharField(max_length=10)
    name = models.CharField(max_length=100, default='')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    availability = models.BooleanField(default=False)
    hospital = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15, default='0')

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=genders, default='Oth')
    phone_number = models.CharField(max_length=15, default='0')

    def __str__(self):
        return self.name
