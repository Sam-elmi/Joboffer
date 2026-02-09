from __future__ import annotations

import logging
import time
from typing import Callable

from django.conf import settings
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("django.request")


class SessionIdleTimeoutMiddleware:
    """Logs out authenticated users after a period of inactivity.

    Safe no-op for anonymous users and when SESSION_IDLE_TIMEOUT is unset.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        timeout = getattr(settings, "SESSION_IDLE_TIMEOUT", None)
        if timeout and request.user.is_authenticated:
            now = int(time.time())
            last_activity = request.session.get("last_activity", now)
            if now - int(last_activity) > int(timeout):
                auth.logout(request)
                request.session.flush()
            else:
                request.session["last_activity"] = now
        return self.get_response(request)


class PermissionDeniedLoggingMiddleware:
    """Logs PermissionDenied exceptions and re-raises them."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception):
        if isinstance(exception, PermissionDenied):
            logger.error("Permission denied", exc_info=exception)
        return None
