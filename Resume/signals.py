import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import BasicInformation, UploadedResume

logger = logging.getLogger('resume')


@receiver(post_save, sender=BasicInformation)
def log_basic_info_save(sender, instance, created, **kwargs):
    if created:
        logger.info("BasicInformation created", extra={"basic_info_id": instance.id, "employee_id": instance.employee_id})
    else:
        logger.info("BasicInformation updated", extra={"basic_info_id": instance.id, "employee_id": instance.employee_id})


@receiver(post_delete, sender=BasicInformation)
def log_basic_info_delete(sender, instance, **kwargs):
    logger.info("BasicInformation deleted", extra={"basic_info_id": instance.id, "employee_id": instance.employee_id})


@receiver(post_save, sender=UploadedResume)
def log_uploaded_resume_save(sender, instance, created, **kwargs):
    if created:
        logger.info("UploadedResume created", extra={"uploaded_resume_id": instance.id, "employee_id": instance.employee_id})
    else:
        logger.info("UploadedResume updated", extra={"uploaded_resume_id": instance.id, "employee_id": instance.employee_id})


@receiver(post_delete, sender=UploadedResume)
def log_uploaded_resume_delete(sender, instance, **kwargs):
    logger.info("UploadedResume deleted", extra={"uploaded_resume_id": instance.id, "employee_id": instance.employee_id})
