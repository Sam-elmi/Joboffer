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


class PersonalInformation(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    register_level = models.ForeignKey(RegisterLevel, on_delete=models.SET_NULL, null=True, blank=True)

    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Employee fields
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # Manager field
    company_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email
