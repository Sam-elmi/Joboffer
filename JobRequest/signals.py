import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import JobRequest

logger = logging.getLogger('jobrequest')


@receiver(post_save, sender=JobRequest)
def log_jobrequest_save(sender, instance, created, **kwargs):
    if created:
        logger.info(
            "JobRequest created",
            extra={"job_request_id": instance.id, "employee_id": instance.employee_id, "job_offer_id": instance.job_offer_id},
        )
    else:
        logger.info(
            "JobRequest updated",
            extra={"job_request_id": instance.id, "employee_id": instance.employee_id, "job_offer_id": instance.job_offer_id},
        )


@receiver(post_delete, sender=JobRequest)
def log_jobrequest_delete(sender, instance, **kwargs):
    logger.info(
        "JobRequest deleted",
        extra={"job_request_id": instance.id, "employee_id": instance.employee_id, "job_offer_id": instance.job_offer_id},
    )
