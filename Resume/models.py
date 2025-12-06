from django.db import models
from Account.models import CustomUser
from django.conf import settings

# 1. Uploaded Resume
class UploadedResume(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_resume',
        #limit_choices_to={'role__name': 'employee'}
    )
    file = models.FileField(upload_to='resumes/', null=True, blank=True)
    is_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"Resume of {self.employee.first_name} {self.employee.last_name}"


# 2. Basic Information
class BasicInformation(models.Model):
    employee = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='basic_info',
        #limit_choices_to={'role__name': 'employee'}
    )

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    MARITAL_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    living_city = models.CharField(max_length=100)
    birth_day = models.DateField()
    expected_salary = models.PositiveIntegerField(null=True, blank=True)
    preferred_job = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Basic Info of {self.employee.first_name} {self.employee.last_name}"


# 3. Study History
#class StudyHistory(models.Model):
#    employee = models.ForeignKey(
 #       settings.AUTH_USER_MODEL,
  #      on_delete=models.CASCADE,
   #     related_name='study_history',
    #    limit_choices_to={'role__name': 'employee'}
    #)
    #university_name = models.CharField(max_length=150)
    #start_date = models.DateField()
    #end_date = models.DateField(null=True, blank=True)
    #grade_of_study = models.CharField(max_length=100)

    #def __str__(self):
     #   return f"{self.university_name} ({self.employee.first_name})"


# 4. Work History
#class WorkHistory(models.Model):
 #   employee = models.ForeignKey(
  #      settings.AUTH_USER_MODEL,
   #     on_delete=models.CASCADE,
    #    related_name='work_history',
     #   limit_choices_to={'role__name': 'employee'}
    #)
   # company_name = models.CharField(max_length=150)
    #duration = models.CharField(max_length=100)
   # work_position = models.CharField(max_length=100)

    #def __str__(self):
     #   return f"{self.work_position} at {self.company_name} ({self.employee.first_name})"


# 5. Languages
#class LanguageSkill(models.Model):
    #employee = models.ForeignKey(
        #settings.AUTH_USER_MODEL,
       # on_delete=models.CASCADE,
      #  related_name='languages',
     #   limit_choices_to={'role__name': 'employee'}
    #)
 #   language_name = models.CharField(max_length=100)
  #  level = models.CharField(max_length=50)

   # def __str__(self):
    #    return f"{self.language_name} ({self.level})"


# 6. Software Skills
#class SoftwareSkill(models.Model):
    #employee = models.ForeignKey(
        #settings.AUTH_USER_MODEL,
       # on_delete=models.CASCADE,
      #  related_name='software_skills',
     #   limit_choices_to={'role__name': 'employee'}
    #)
    #software_name = models.CharField(max_length=100)
    #level = models.CharField(max_length=50, help_text="Example: Beginner / Intermediate / Expert")

   # def __str__(self):
    #    return f"{self.software_name} ({self.level})"
#