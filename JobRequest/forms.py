# forms.py
from django import forms
from .models import JobRequest, JobOffer

class JobRequestForm(forms.ModelForm):
    """
    فرم ثبت درخواست جدید توسط کارمند
    """
    class Meta:
        model = JobRequest
        fields = [
            'job_offer',
            'requested_salary',
        ]
        widgets = {
            'job_offer': forms.Select(attrs={'class': 'form-control'}),
            'requested_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'حقوق درخواستی'}),
        }

    def save(self, commit=True, employee=None):
        obj = super().save(commit=False)
        if employee:
            obj.employee = employee
        # سایر فیلدهای خودکار توسط save مدل پر می‌شوند
        if commit:
            obj.save()
        return obj


class JobRequestUpdateForm(forms.ModelForm):
    """
    فرم ویرایش درخواست، فقط اجازه ویرایش حقوق درخواستی
    """
    class Meta:
        model = JobRequest
        fields = [
            'requested_salary',
        ]
        widgets = {
            'requested_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'حقوق درخواستی'}),
        }

    # اگر نیاز باشه، save می‌تواند تغییرات اضافی مدیریت را اعمال کند
    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
        return obj
