from django.db import models
from django.conf import settings

# 1. Uploaded Resume
class UploadedResume(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_resume',
        #limit_choices_to={'role__name': 'employee'}
    )
    file = models.FileField(upload_to='resumes/', null=True, blank=True)
    is_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"Resume of {self.employee.first_name} {self.employee.last_name}"


# 2. Basic Information
class BasicInformation(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basic_info',
        #limit_choices_to={'role__name': 'employee'}
    )

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    MARITAL_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    living_city = models.CharField(max_length=100)
    birth_day = models.DateField()
    expected_salary = models.PositiveIntegerField(null=True, blank=True)
    preferred_job = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Basic Info of {self.employee.first_name} {self.employee.last_name}"
