from django import forms
from .models import BasicInformation, UploadedResume

class BasicInformationForm(forms.ModelForm):
    class Meta:
        model = BasicInformation
        fields = [
            'gender',
            'marital_status',
            'living_city',
            'birth_day',
            'expected_salary',
            'preferred_job',
        ]
        widgets = {
            'birth_day': forms.DateInput(attrs={'type': 'date'}),
        }

class UploadedResumeForm(forms.ModelForm):
    class Meta:
        model = UploadedResume
        fields = ['file']
