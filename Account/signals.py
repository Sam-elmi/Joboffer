import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.core.signals import got_request_exception
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger('account')
User = get_user_model()


def _get_client_ip(request):
    if not request:
        return None
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = _get_client_ip(request)
    logger.info("User logged in", extra={"user_id": user.id, "email": user.email, "ip": ip})
    if request is not None:
        request.session['login_at'] = timezone.now().isoformat()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = _get_client_ip(request)
    user_id = getattr(user, 'id', None)
    email = getattr(user, 'email', None)
    logger.info("User logged out", extra={"user_id": user_id, "email": email, "ip": ip})


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = _get_client_ip(request)
    identifier = credentials.get('email') or credentials.get('username')
    logger.warning("User login failed", extra={"identifier": identifier, "ip": ip})


@receiver(got_request_exception)
def log_server_error(sender, request, **kwargs):
    ip = _get_client_ip(request)
    user = getattr(request, 'user', None)
    logger.exception(
        "Server error",
        extra={"path": getattr(request, 'path', None), "user_id": getattr(user, 'id', None), "ip": ip},
    )


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    if created:
        logger.info("User created", extra={"user_id": instance.id, "email": instance.email})
    else:
        logger.info("User updated", extra={"user_id": instance.id, "email": instance.email})


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    logger.info("User deleted", extra={"user_id": instance.id, "email": instance.email})
