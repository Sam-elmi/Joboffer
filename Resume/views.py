from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import BasicInformation, UploadedResume
from .forms import BasicInformationForm, UploadedResumeForm
from Account.models import CustomUser

class ResumeHomeView(TemplateView):
    template_name = 'resume/home.html'

class ResumeListView(ListView):
    model = CustomUser
    template_name = 'resume/resume_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return CustomUser.objects.all().order_by('first_name', 'last_name')


class ResumeDetailView(DetailView):
    model = CustomUser
    template_name = 'resume/resume_detail.html'
    context_object_name = 'employee'

    def get_queryset(self):
        return CustomUser.objects.filter(role__name='employee')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.object
        context['uploaded_resume'] = getattr(employee, 'uploaded_resume', None)
        context['basic_info'] = getattr(employee, 'basic_info', None)
        return context

@login_required
def ResumeInfoView(request):
    user = request.user

    # نمونه موجود یا None
    basic_instance = getattr(user, 'basic_info', None)
    resume_instance = getattr(user, 'uploaded_resume', None)

    if request.method == 'POST':
        basic_form = BasicInformationForm(request.POST, instance=basic_instance)
        resume_form = UploadedResumeForm(request.POST, request.FILES, instance=resume_instance)

        if basic_form.is_valid() and resume_form.is_valid():
            basic = basic_form.save(commit=False)
            basic.employee = user
            basic.save()

            resume = resume_form.save(commit=False)
            resume.employee = user
            resume.save()

            # بعد از ثبت، بریم صفحه لیست رزومه‌ها
            return redirect('resume:resume_list')

    else:
        basic_form = BasicInformationForm(instance=basic_instance)
        resume_form = UploadedResumeForm(instance=resume_instance)

    return render(request, 'resume/resume_info_form.html', {
        'basic_form': basic_form,
        'resume_form': resume_form,
    })
