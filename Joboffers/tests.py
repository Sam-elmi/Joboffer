from django.test import TestCase
from django.urls import reverse

from Account.models import CustomUser, UserRole, RegisterLevel
from .models import JobOffer, JobPosition, JobCategory


class JobOfferManagerTests(TestCase):
    def setUp(self):
        self.role_employer = UserRole.objects.create(name='employer')
        self.level = RegisterLevel.objects.create(level='base')
        self.employer = CustomUser.objects.create(
            email='employer@example.com',
            role=self.role_employer,
            register_level=self.level,
            is_active=True,
        )
        self.employer.set_password('TestPass123!')
        self.employer.save()

        self.position = JobPosition.objects.create(name='Backend Developer')
        self.category = JobCategory.objects.create(name='Software')

        JobOffer.objects.create(
            manager=self.employer,
            company_name='Acme',
            job_position=self.position,
            job_category=self.category,
            cooperation_type='fulltime',
            work_indicators='Python',
            job_explanation='Build APIs',
            status='available',
        )
        JobOffer.objects.create(
            manager=self.employer,
            company_name='Acme',
            job_position=self.position,
            job_category=self.category,
            cooperation_type='fulltime',
            work_indicators='Django',
            job_explanation='Maintain apps',
            status='expired',
        )

    def test_manager_filters(self):
        self.assertEqual(JobOffer.objects.active().count(), 1)
        self.assertEqual(JobOffer.objects.expired().count(), 1)
        self.assertEqual(JobOffer.objects.by_employer(self.employer).count(), 2)

    def test_offer_list_template_includes_base(self):
        response = self.client.get(reverse('joboffers:offer_list'))
        self.assertContains(response, 'سامانه مدیریت آگهی‌های شغلی')
