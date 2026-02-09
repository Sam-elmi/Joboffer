import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import JobOffer, JobCategory, JobPosition

logger = logging.getLogger('joboffers')


@receiver(post_save, sender=JobOffer)
def log_joboffer_save(sender, instance, created, **kwargs):
    if created:
        logger.info("JobOffer created", extra={"job_offer_id": instance.id, "manager_id": instance.manager_id})
    else:
        logger.info("JobOffer updated", extra={"job_offer_id": instance.id, "manager_id": instance.manager_id})


@receiver(post_delete, sender=JobOffer)
def log_joboffer_delete(sender, instance, **kwargs):
    logger.info("JobOffer deleted", extra={"job_offer_id": instance.id, "manager_id": instance.manager_id})


@receiver(post_save, sender=JobCategory)
def log_jobcategory_save(sender, instance, created, **kwargs):
    if created:
        logger.info("JobCategory created", extra={"job_category_id": instance.id, "job_category_name": instance.name})
    else:
        logger.info("JobCategory updated", extra={"job_category_id": instance.id, "job_category_name": instance.name})


@receiver(post_delete, sender=JobCategory)
def log_jobcategory_delete(sender, instance, **kwargs):
    logger.info("JobCategory deleted", extra={"job_category_id": instance.id, "job_category_name": instance.name})


@receiver(post_save, sender=JobPosition)
def log_jobposition_save(sender, instance, created, **kwargs):
    if created:
        logger.info("JobPosition created", extra={"job_position_id": instance.id, "job_position_name": instance.name})
    else:
        logger.info("JobPosition updated", extra={"job_position_id": instance.id, "job_position_name": instance.name})


@receiver(post_delete, sender=JobPosition)
def log_jobposition_delete(sender, instance, **kwargs):
    logger.info("JobPosition deleted", extra={"job_position_id": instance.id, "job_position_name": instance.name})
