from django import forms
from .models import CustomUser, UserRole, RegisterLevel

class PersonalInformationForm(forms.ModelForm):
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput,
        required=False  # حالا برای ویرایش اختیاری است
    )

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'phone_number',
            'role',
            'register_level',
            'first_name',
            'last_name',
            'company_name'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # مقدار پیش‌فرض برای role و register_level
        if not self.instance.role:
            first_role = UserRole.objects.first()
            if first_role:
                self.instance.role = first_role

        if not self.instance.register_level:
            first_level = RegisterLevel.objects.first()
            if first_level:
                self.instance.register_level = first_level

        # غیرفعال کردن فیلدها بر اساس role
        if self.instance.role:
            if self.instance.role.name == 'employee':
                self.fields['role'].disabled = True
                self.fields['company_name'].disabled = True
            elif self.instance.role.name == 'manager':
                self.fields['role'].disabled = True
                self.fields['first_name'].disabled = True
                self.fields['last_name'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role and role.name == 'employee':
            if not cleaned_data.get('first_name') or not cleaned_data.get('last_name'):
                raise forms.ValidationError("برای کارمند، نام و نام خانوادگی باید پر شود.")
        elif role and role.name == 'manager':
            if not cleaned_data.get('company_name'):
                raise forms.ValidationError("برای مدیر، نام شرکت باید پر شود.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # اگر رمز عبور وارد شده باشد، هش کن و ذخیره کن
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
