from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import PersonalInformationForm
from django.contrib.auth.views import LoginView


class AccountHomeView(TemplateView):
    template_name = 'account/home.html'


class PersonalInfoListView(ListView):
    model = CustomUser
    template_name = 'account/personal_info_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.select_related('role', 'register_level')


class PersonalInfoDetailView(DetailView):
    model = CustomUser
    template_name = 'account/personal_info_detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        return CustomUser.objects.select_related('role', 'register_level')


class PersonalInfoCreateView(CreateView):
    model = CustomUser
    form_class = PersonalInformationForm
    template_name = 'account/personal_info_form.html'
    success_url = reverse_lazy('account:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        # هش کردن پسورد
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class PersonalInfoUpdateView(UpdateView):
    model = CustomUser
    form_class = PersonalInformationForm
    template_name = 'account/personal_info_form.html'
    success_url = reverse_lazy('account:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data.get('password'):
            user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'account/login.html'  # مسیر تمپلیت لاگین

    def get_success_url(self):
        """
        بعد از ورود موفق، کاربر را به صفحه جزئیات خودش هدایت می‌کند.
        """
        return reverse_lazy('account:user_detail', kwargs={'pk': self.request.user.pk})
