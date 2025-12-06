from django.views.generic import TemplateView, ListView, DetailView , CreateView, UpdateView
from .models import JobRequest
from django.urls import reverse_lazy
from .forms import JobRequestForm, JobRequestUpdateForm

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


class JobRequestCreateView(CreateView):
    model = JobRequest
    form_class = JobRequestForm
    template_name = 'jobrequest/jobrequest_form.html'

    def form_valid(self, form):
        self.object = form.save(employee=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        # هدایت به صفحه لیست درخواست‌ها بعد از ثبت
        return reverse_lazy('jobrequest:request_list')


# ویرایش درخواست موجود
class JobRequestUpdateView(UpdateView):
    model = JobRequest
    form_class = JobRequestUpdateForm
    template_name = 'jobrequest/jobrequest_form.html'

    def get_success_url(self):
        # هدایت به صفحه لیست درخواست‌ها بعد از ویرایش
        return reverse_lazy('jobrequest:request_list')
