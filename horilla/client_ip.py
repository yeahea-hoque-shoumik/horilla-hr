"""Resolve the real client IP for deployments behind a Cloudflare Tunnel."""

import ipaddress
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed

logger = logging.getLogger(__name__)

# A client can send any of these. They are removed so that nothing downstream
# (DRF throttling, audit log, django-axes) can read a forged value.
FORWARDING_HEADERS = ("HTTP_X_FORWARDED_FOR", "HTTP_X_REAL_IP", "HTTP_FORWARDED")


def _parse_networks(values):
    try:
        return [ipaddress.ip_network(value.strip(), strict=False) for value in values]
    except ValueError as error:
        raise ImproperlyConfigured(f"Invalid TRUSTED_PROXY_IPS: {error}") from error


def _parse_ip(value):
    try:
        return ipaddress.ip_address((value or "").strip())
    except ValueError:
        return None


class TrustedProxyClientIPMiddleware:
    """
    Set REMOTE_ADDR to CF-Connecting-IP when the connection comes from a
    trusted proxy, and ignore that header from anyone else.

    request.META is gunicorn's WSGI environ, so its access log reports the
    same address. Inactive while TRUSTED_PROXY_IPS is empty.
    """

    def __init__(self, get_response):
        configured = getattr(settings, "TRUSTED_PROXY_IPS", [])
        if not configured:
            raise MiddlewareNotUsed
        self.get_response = get_response
        self.trusted_networks = _parse_networks(configured)

    def _is_trusted(self, peer):
        return peer is not None and any(
            peer.version == network.version and peer in network
            for network in self.trusted_networks
        )

    def __call__(self, request):
        meta = request.META
        cloudflare_ip = meta.pop("HTTP_CF_CONNECTING_IP", None)
        for header in FORWARDING_HEADERS:
            meta.pop(header, None)

        peer = meta.get("REMOTE_ADDR")
        if self._is_trusted(_parse_ip(peer)):
            client = _parse_ip(cloudflare_ip)
            if client is None:
                logger.warning("Trusted proxy sent no valid CF-Connecting-IP")
            else:
                meta["horilla.proxy_peer"] = peer
                meta["REMOTE_ADDR"] = str(client)
        return self.get_response(request)
