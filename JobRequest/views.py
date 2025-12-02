from django.views.generic import TemplateView, ListView, DetailView
from .models import JobRequest


class JobRequestHomeView(TemplateView):
    template_name = 'jobrequest/home.html'


class JobRequestListView(ListView):
    model = JobRequest
    template_name = 'jobrequest/jobrequest_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        # جدیدترین درخواست‌ها بالا
        return (
            JobRequest.objects
            .select_related('employee', 'job_offer', 'job_position')
            .order_by('-created_at')
        )


class JobRequestDetailView(DetailView):
    model = JobRequest
    template_name = 'jobrequest/jobrequest_detail.html'
    context_object_name = 'request_obj'

    def get_queryset(self):
        return JobRequest.objects.select_related('employee', 'job_offer', 'job_position')
