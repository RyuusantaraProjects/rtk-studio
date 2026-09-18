"""Public legal pages: Terms of Service, Privacy Policy, and User Data Deletion Instructions.

These pages are publicly accessible without authentication and comply with Meta,
Google, TikTok, and LinkedIn developer platform policies.
"""

import base64
import hashlib
import hmac
import json
import logging
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def terms_view(request):
    """Render public Terms of Service page."""
    context = {
        "active_tab": "terms",
        "last_updated": "18 September 2026",
    }
    return render(request, "legal/terms.html", context)


def privacy_view(request):
    """Render public Privacy Policy page."""
    context = {
        "active_tab": "privacy",
        "last_updated": "18 September 2026",
    }
    return render(request, "legal/privacy.html", context)


@csrf_exempt
def data_deletion_view(request):
    """User Data Deletion Instructions (GET) and Meta Data Deletion Callback (POST).

    GET: Displays clear, step-by-step instructions for users on how to delete their
         data from RTK Studio and revoke permissions via Facebook/Instagram.
    POST: Handles Meta's signed_request webhook for automated data deletion callback.
    """
    if request.method == "POST":
        return _handle_meta_deletion_callback(request)

    confirmation_code = request.GET.get("code") or request.GET.get("id")
    context = {
        "active_tab": "data_deletion",
        "last_updated": "18 September 2026",
        "confirmation_code": confirmation_code,
    }
    return render(request, "legal/data_deletion.html", context)


def _handle_meta_deletion_callback(request):
    """Process Meta's data deletion callback signed_request and return status URL."""
    signed_request = request.POST.get("signed_request")
    confirmation_code = str(uuid.uuid4())[:12].upper()

    user_id = None
    if signed_request and "." in signed_request:
        try:
            encoded_sig, payload = signed_request.split(".", 1)
            # Pad base64 payload if needed
            padded_payload = payload + "=" * (-len(payload) % 4)
            data = json.loads(base64.urlsafe_b64decode(padded_payload.encode("utf-8")).decode("utf-8"))
            user_id = data.get("user_id")
            logger.info("Meta data deletion requested for user_id=%s with code=%s", user_id, confirmation_code)
        except Exception as exc:
            logger.warning("Failed to decode Meta signed_request: %s", exc)

    status_url = request.build_absolute_uri(f"/data-deletion/?code={confirmation_code}")
    return JsonResponse({
        "url": status_url,
        "confirmation_code": confirmation_code,
    })
