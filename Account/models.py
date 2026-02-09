# Account/models.py
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    # ---- Query helpers (همون چیزهایی که داشتی) ----
    def employers(self):
        return self.filter(role__name='employer')

    def applicants(self):
        return self.filter(role__name='applicant')

    def active_users(self):
        return self.filter(is_active=True)

    def unverified_users(self):
        return self.filter(is_active=False)

    # ---- Auth-required methods ----
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
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
    username = None  # ایمیل شناسه لاگین است
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    register_level = models.ForeignKey(RegisterLevel, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # Employee fields
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # Manager field
    company_name = models.CharField(max_length=100, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
