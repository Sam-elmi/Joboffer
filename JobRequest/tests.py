from django.test import TestCase

from Account.models import CustomUser, UserRole, RegisterLevel
from joboffers.models import JobOffer, JobPosition, JobCategory
from .models import JobRequest


class JobRequestManagerTests(TestCase):
    def setUp(self):
        self.role_employer = UserRole.objects.create(name='employer')
        self.role_applicant = UserRole.objects.create(name='applicant')
        self.level = RegisterLevel.objects.create(level='base')

        self.employer = CustomUser.objects.create(
            email='employer@example.com',
            role=self.role_employer,
            register_level=self.level,
            is_active=True,
            company_name='Acme',
        )
        self.employer.set_password('TestPass123!')
        self.employer.save()

        self.applicant = CustomUser.objects.create(
            email='applicant@example.com',
            role=self.role_applicant,
            register_level=self.level,
            is_active=True,
            first_name='Ali',
            last_name='Test',
        )
        self.applicant.set_password('TestPass123!')
        self.applicant.save()

        self.position = JobPosition.objects.create(name='Backend Developer')
        self.category = JobCategory.objects.create(name='Software')

        self.offer = JobOffer.objects.create(
            manager=self.employer,
            company_name='Acme',
            job_position=self.position,
            job_category=self.category,
            cooperation_type='fulltime',
            work_indicators='Python',
            job_explanation='Build APIs',
            status='available',
        )

        JobRequest.objects.create(
            employee=self.applicant,
            job_offer=self.offer,
            job_position=self.position,
            company_name='Acme',
            employee_first_name='Ali',
            employee_last_name='Test',
            requested_salary=1000,
            status='checking',
        )
        JobRequest.objects.create(
            employee=self.applicant,
            job_offer=self.offer,
            job_position=self.position,
            company_name='Acme',
            employee_first_name='Ali',
            employee_last_name='Test',
            requested_salary=1000,
            status='accepted',
        )
        JobRequest.objects.create(
            employee=self.applicant,
            job_offer=self.offer,
            job_position=self.position,
            company_name='Acme',
            employee_first_name='Ali',
            employee_last_name='Test',
            requested_salary=1000,
            status='rejected',
        )

    def test_manager_filters(self):
        self.assertEqual(JobRequest.objects.pending().count(), 1)
        self.assertEqual(JobRequest.objects.accepted().count(), 1)
        self.assertEqual(JobRequest.objects.rejected().count(), 1)
