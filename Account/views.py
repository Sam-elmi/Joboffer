from django.views.generic import TemplateView, ListView, DetailView
from .models import PersonalInformation
from django.shortcuts import get_object_or_404


class AccountHomeView(TemplateView):
    template_name = 'account/home.html'


class PersonalInfoListView(ListView):
    model = PersonalInformation
    template_name = 'account/personal_info_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return PersonalInformation.objects.select_related('role', 'register_level')


class PersonalInfoDetailView(DetailView):
    model = PersonalInformation
    template_name = 'account/personal_info_detail.html'
    context_object_name = 'user'
    
    def get_queryset(self):
        return PersonalInformation.objects.select_related('role', 'register_level')


