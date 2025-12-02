from django.views.generic import TemplateView, ListView, DetailView
from .models import UserPanel


class UserPanelHomeView(TemplateView):
    template_name = 'userpanel/home.html'


class UserPanelListView(ListView):
    """
    لیست همهٔ پنل‌های کاربران، برای تست و مدیریت
    """
    model = UserPanel
    template_name = 'userpanel/panel_list.html'
    context_object_name = 'panels'

    def get_queryset(self):
        return UserPanel.objects.select_related('user').order_by('user__email')


class UserPanelDetailView(DetailView):
    """
    نمایش پنل یک کاربر:
      - اگر manager باشد → آگهی‌های شرکت + همهٔ درخواست‌های مربوط به شرکت
      - اگر employee باشد → فقط درخواست‌های خودش
    """
    model = UserPanel
    template_name = 'userpanel/panel_detail.html'
    context_object_name = 'panel'

    def get_queryset(self):
        return UserPanel.objects.select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panel = self.object
        user = panel.user

        job_offers = panel.get_job_offers()
        job_requests = panel.get_job_requests()

        context['job_offers'] = job_offers
        context['job_requests'] = job_requests
        context['is_manager'] = bool(user.company_name)

        return context
