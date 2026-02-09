from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import CustomUser, UserRole, RegisterLevel
from .tokens import account_activation_token


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RegistrationActivationTests(TestCase):
    def setUp(self):
        self.role_applicant = UserRole.objects.create(name='applicant')
        self.level = RegisterLevel.objects.create(level='base')

    def test_registration_creates_inactive_user_and_sends_email(self):
        response = self.client.post(
            reverse('account:user_add'),
            data={
                'email': 'newuser@example.com',
                'password': 'TestPass123!',
                'role': self.role_applicant.id,
                'register_level': self.level.id,
                'first_name': 'Test',
                'last_name': 'User',
            },
        )
        self.assertRedirects(response, reverse('account:user_list'))
        user = CustomUser.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('activate', mail.outbox[0].body)

    def test_activation_changes_user_to_active(self):
        user = CustomUser.objects.create(
            email='inactive@example.com',
            role=self.role_applicant,
            register_level=self.level,
            is_active=False,
            first_name='In',
            last_name='Active',
        )
        user.set_password('TestPass123!')
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        response = self.client.get(reverse('account:activate', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_base_template_renders(self):
        response = self.client.get(reverse('account:home'))
        self.assertContains(response, 'سامانه مدیریت آگهی‌های شغلی')
