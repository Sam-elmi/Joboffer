from django.db import models
from Account.models import PersonalInformation
from Joboffers.models import JobOffer
from JobRequest.models import JobRequest


class UserPanel(models.Model):
    user = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        related_name='user_panel'
    )

    def __str__(self):
        return f"Panel of {self.user.email}"

    # Managers → see all JobOffers & JobRequests under their company
    # Employees → see only their own JobRequests
    def get_job_offers(self):
        if self.user.company_name:
            return JobOffer.objects.filter(manager__company_name=self.user.company_name)
        return JobOffer.objects.none()

    def get_job_requests(self):
        if self.user.company_name:
            # Manager: all requests related to this company’s job offers
            return JobRequest.objects.filter(company_name=self.user.company_name)
        else:
            # Employee: only requests they personally made
            return JobRequest.objects.filter(
                employee_first_name=self.user.first_name,
                employee_last_name=self.user.last_name
            )
