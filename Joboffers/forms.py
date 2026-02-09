# forms.py
from django import forms
from .models import JobOffer, JobPosition, JobCategory


class JobOfferForm(forms.ModelForm):
    # کاربر عنوان شغلی را وارد می‌کند و اگر وجود نداشت ساخته شود
    job_position_name = forms.CharField(
        label="عنوان شغل",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'عنوان شغلی را وارد کنید'})
    )

    # فیلد نام شرکت برای ثبت در هنگام ثبت آگهی
    company_name = forms.CharField(
        label="نام شرکت",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'نام شرکت خود را وارد کنید'})
    )

    class Meta:
        model = JobOffer
        fields = [
            'job_position',  # این فیلد از طریق job_position_name پر خواهد شد
            'job_category',
            'work_day',
            'work_time',
            'cooperation_type',
            'work_indicators',
            'job_explanation',
            'age_limit',
            'gender',
        ]
        widgets = {
            'job_category': forms.Select(),
            'work_indicators': forms.Textarea(attrs={'rows': 3}),
            'job_explanation': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True, manager=None):
        # گرفتن شیء از ModelForm
        obj = super().save(commit=False)

        # ایجاد یا گرفتن JobPosition از نام وارد شده
        position_name = self.cleaned_data.get("job_position_name")
        if position_name:
            position_obj, created = JobPosition.objects.get_or_create(name=position_name)
            obj.job_position = position_obj

        # اختصاص دادن مدیر
        if manager:
            obj.manager = manager

        company_name = self.cleaned_data.get("company_name")
        if company_name:
            obj.company_name = company_name

        if commit:
            obj.save()
        return obj
