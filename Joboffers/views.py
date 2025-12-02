from django.views.generic import ListView, DetailView
from .models import JobOffer, JobPosition, JobCategory


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
        return JobOffer.objects.select_related('manager', 'job_position', 'job_category')


class JobPositionListView(ListView):
    model = JobPosition
    template_name = 'joboffers/jobposition_list.html'
    context_object_name = 'positions'

    def get_queryset(self):
        return JobPosition.objects.all().order_by('name')


class JobCategoryListView(ListView):
    model = JobCategory
    template_name = 'joboffers/jobcategory_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return JobCategory.objects.all().order_by('name')
