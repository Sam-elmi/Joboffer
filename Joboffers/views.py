from django.views.generic import ListView, DetailView, CreateView, DeleteView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import JobOffer, JobCategory
from .forms import JobOfferForm

class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return (
            JobOffer.objects
            .select_related('manager', 'job_position', 'job_category')
            .filter(status='available')
            .order_by('-created_at')
        )


class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = 'joboffers/joboffer_detail.html'
    context_object_name = 'offer'

    def get_queryset(self):
        return JobOffer.objects.select_related(
            'manager', 'job_position', 'job_category'
        )


class JobOfferCreateView(LoginRequiredMixin, CreateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = "joboffers/joboffer_form.html"
    success_url = reverse_lazy("joboffers:offer_list")

    def form_valid(self, form):
        form.save(manager=self.request.user)
        return super().form_valid(form)



class JobCategoryListView(ListView):
    model = JobCategory
    template_name = 'joboffers/jobcategory_list.html'
    context_object_name = 'categories'

class JobCategoryCreateView(CreateView):
    model = JobCategory
    fields = ['name']  # فقط فیلد نام
    template_name = 'joboffers/jobcategory_form.html'
    success_url = reverse_lazy('joboffers:category_list')



class JobOfferUpdateView(UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'joboffers/joboffer_form.html'
    success_url = reverse_lazy('joboffers:offer_list')






class JobOfferDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        model = JobOffer
        template_name = 'joboffers/joboffer_confirm_delete.html'
        success_url = reverse_lazy('joboffers:offer_list')

        def test_func(self):
            offer = self.get_object()
            return self.request.user == offer.manager
