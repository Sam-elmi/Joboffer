from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from Account.models import PersonalInformation
from .models import (
    UploadedResume,
    BasicInformation,
    StudyHistory,
    WorkHistory,
    LanguageSkill,
    SoftwareSkill,
)


class ResumeHomeView(TemplateView):
    template_name = 'resume/home.html'


class ResumeListView(ListView):
    """
    لیست همه‌ی employeeها که نقش‌شان employee است
    """
    model = PersonalInformation
    template_name = 'resume/resume_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        # فقط کسانی که role = employee دارند
        return PersonalInformation.objects.filter(role__name='employee').order_by('first_name', 'last_name')


class ResumeDetailView(DetailView):
    """
    نمایش جزئیات رزومه یک employee
    """
    model = PersonalInformation
    template_name = 'resume/resume_detail.html'
    context_object_name = 'employee'

    def get_queryset(self):
        # فقط employeeها
        return PersonalInformation.objects.filter(role__name='employee')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.object

        # بخش‌های مختلف رزومه
        context['uploaded_resume'] = getattr(employee, 'uploaded_resume', None)
        context['basic_info'] = getattr(employee, 'basic_info', None)
        context['study_history_list'] = employee.study_history.all()
        context['work_history_list'] = employee.work_history.all()
        context['language_list'] = employee.languages.all()
        context['software_skill_list'] = employee.software_skills.all()

        return context
