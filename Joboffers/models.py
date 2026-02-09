from django.db import models
from Account.models import CustomUser
from django.conf import settings

class JobOfferManager(models.Manager):
    def active(self):
        return self.filter(status='available')

    def expired(self):
        return self.filter(status='expired')

    def by_employer(self, user):
        return self.filter(manager=user)

class JobPosition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class JobOffer(models.Model):
    COOPERATION_CHOICES = [
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('remote', 'Remote'),
        ('project', 'Project-Based'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('expired', 'Expired'),
    ]

    # Linked to the manager who posts the job
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_offers',
        limit_choices_to={'role__name': 'employer'}  # restrict only to employer users
    )

    # فیلد جدید برای وارد کردن اسم شرکت هنگام ثبت آگهی
    company_name = models.CharField(max_length=200, null=True, blank=True)

    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)

    work_day = models.CharField(max_length=100, null=True, blank=True)
    work_time = models.CharField(max_length=100, null=True, blank=True)
    cooperation_type = models.CharField(max_length=20, choices=COOPERATION_CHOICES)

    work_indicators = models.TextField(help_text="List of skills or requirements")
    job_explanation = models.TextField(help_text="Detailed description of the job")

    # Optional conditions
    age_limit = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobOfferManager()

    def __str__(self):
        # نمایش نام شرکت از فیلد جدید، در صورت عدم وجود مقدار، Unknown Company
        company = self.company_name if self.company_name else "Unknown Company"
        return f"{self.job_position.name} at {company}"
