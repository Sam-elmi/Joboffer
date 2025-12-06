from django.db import models
from Account.models import CustomUser
from joboffers.models import JobOffer, JobPosition
from django.conf import settings

class JobRequest(models.Model):
    STATUS_CHOICES = [
        ('checking', 'Checking'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    REQUEST_CHECK_CHOICES = [
        ('checked', 'Checked'),
        ('not_checked', 'Not Checked'),
    ]

    # Relations
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_requests',
        limit_choices_to={'role__name': 'employee'}
    )

    job_offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Info fetched from Account (via relations)
    company_name = models.CharField(max_length=150)
    employee_first_name = models.CharField(max_length=50)
    employee_last_name = models.CharField(max_length=50)

    requested_salary = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='checking')
    request_check = models.CharField(max_length=20, choices=REQUEST_CHECK_CHOICES, default='not_checked')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.employee_first_name} {self.employee_last_name} for {self.job_position}"

    def save(self, *args, **kwargs):
        """
        Auto-fill company name and employee info from related models.
        """
        # Get company name from job_offer.manager
        if self.job_offer and self.job_offer.manager:
            self.company_name = self.job_offer.manager.company_name or "Unknown"

        # Get employee info
        if self.employee:
            self.employee_first_name = self.employee.first_name or ""
            self.employee_last_name = self.employee.last_name or ""

        # Get job position name
        if not self.job_position and self.job_offer:
            self.job_position = self.job_offer.job_position

        super().save(*args, **kwargs)
