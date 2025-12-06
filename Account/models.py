# Account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    def __str__(self):
        return self.get_name_display()

class RegisterLevel(models.Model):
    LEVEL_CHOICES = [
        ('base', 'Base Level'),
        ('medium', 'Medium Level'),
        ('full', 'Full Level'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)
    def __str__(self):
        return self.get_level_display()

class CustomUser(AbstractUser):
    username = None  # ما ایمیل رو به عنوان شناسه لاگین گرفتیم
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    register_level = models.ForeignKey(RegisterLevel, on_delete=models.SET_NULL, null=True, blank=True)

    # Employee fields
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # Manager field
    company_name = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
