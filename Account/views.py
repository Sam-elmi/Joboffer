import logging

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from .forms import PersonalInformationForm
from .tokens import account_activation_token

logger = logging.getLogger('account')
User = get_user_model()

class AccountHomeView(TemplateView):
    template_name = 'account/home.html'


class PersonalInfoListView(ListView):
    model = User
    template_name = 'account/personal_info_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.select_related('role', 'register_level')


class PersonalInfoDetailView(DetailView):
    model = User
    template_name = 'account/personal_info_detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.select_related('role', 'register_level')


class PersonalInfoCreateView(CreateView):
    model = User
    form_class = PersonalInformationForm
    template_name = 'account/personal_info_form.html'
    success_url = reverse_lazy('account:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.object = user
        self._send_activation_email(user)
        messages.success(self.request, "ثبت‌نام انجام شد. لطفا ایمیل خود را برای فعال‌سازی بررسی کنید.")
        logger.info("User created via form", extra={"user_id": user.id, "email": user.email})
        return redirect(self.get_success_url())

    def _send_activation_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse('account:activate', kwargs={'uidb64': uid, 'token': token})
        )
        subject = "فعالسازی حساب کاربری"
        message = render_to_string(
            'account/activation_email.txt',
            {'user': user, 'activation_link': activation_link},
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class PersonalInfoUpdateView(UpdateView):
    model = User
    form_class = PersonalInformationForm
    template_name = 'account/personal_info_form.html'
    success_url = reverse_lazy('account:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info("User updated via form", extra={"user_id": self.object.id, "email": self.object.email})
        return response

class CustomLoginView(LoginView):
    template_name = 'account/login.html'  # مسیر تمپلیت لاگین

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "ورود با موفقیت انجام شد.")
        return response

    def get_success_url(self):
        """
        بعد از ورود موفق، کاربر را به صفحه جزئیات خودش هدایت می‌کند.
        """
        return reverse_lazy('account:user_detail', kwargs={'pk': self.request.user.pk})


def activate_account(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and user.is_active:
        messages.info(request, "این حساب قبلا فعال شده است.")
        status = "already_active"
    elif user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "حساب کاربری شما با موفقیت فعال شد.")
        status = "activated"
    else:
        messages.error(request, "لینک فعال‌سازی معتبر نیست یا منقضی شده است.")
        status = "invalid"

    return render(request, 'account/activation_result.html', {'activation_status': status})
