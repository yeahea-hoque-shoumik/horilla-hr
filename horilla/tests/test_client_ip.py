"""Client IP resolution behind a Cloudflare Tunnel."""

from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from attendance.methods.utils import get_client_ip
from horilla.client_ip import TrustedProxyClientIPMiddleware

CONNECTOR = "192.168.0.132"
CLIENT = "103.239.252.115"
FORGED = "1.2.3.4"


@override_settings(
    TRUSTED_PROXY_IPS=[CONNECTOR],
    AXES_IPWARE_PROXY_COUNT=None,
    AXES_IPWARE_META_PRECEDENCE_ORDER=["REMOTE_ADDR"],
)
class TrustedProxyClientIPTests(SimpleTestCase):
    def resolve(self, peer=CONNECTOR, **headers):
        request = RequestFactory().get("/", REMOTE_ADDR=peer, **headers)
        TrustedProxyClientIPMiddleware(lambda _request: HttpResponse())(request)
        return request

    def test_connector_uses_cloudflare_ip(self):
        request = self.resolve(HTTP_CF_CONNECTING_IP=CLIENT)
        self.assertEqual(request.META["REMOTE_ADDR"], CLIENT)
        self.assertEqual(request.META["horilla.proxy_peer"], CONNECTOR)
        self.assertEqual(get_client_ip(request), CLIENT)

    def test_forged_forwarded_for_is_ignored(self):
        request = self.resolve(
            HTTP_CF_CONNECTING_IP=CLIENT,
            HTTP_X_FORWARDED_FOR=f"{FORGED}, {CLIENT}",
            HTTP_X_REAL_IP=FORGED,
        )
        self.assertEqual(get_client_ip(request), CLIENT)
        self.assertNotIn("HTTP_X_FORWARDED_FOR", request.META)
        self.assertNotIn("HTTP_X_REAL_IP", request.META)

    def test_direct_lan_client_cannot_forge_cloudflare_header(self):
        request = self.resolve(peer="192.168.0.50", HTTP_CF_CONNECTING_IP=FORGED)
        self.assertEqual(get_client_ip(request), "192.168.0.50")
        self.assertNotIn("HTTP_CF_CONNECTING_IP", request.META)

    def test_invalid_cloudflare_value_keeps_peer(self):
        with self.assertLogs("horilla.client_ip", "WARNING"):
            request = self.resolve(HTTP_CF_CONNECTING_IP="not-an-ip")
        self.assertEqual(request.META["REMOTE_ADDR"], CONNECTOR)

    def test_missing_cloudflare_value_keeps_peer(self):
        with self.assertLogs("horilla.client_ip", "WARNING"):
            request = self.resolve()
        self.assertEqual(request.META["REMOTE_ADDR"], CONNECTOR)

    def test_ipv6_client(self):
        request = self.resolve(HTTP_CF_CONNECTING_IP="2001:db8::1")
        self.assertEqual(get_client_ip(request), "2001:db8::1")

    @override_settings(TRUSTED_PROXY_IPS=["192.168.0.0/24"])
    def test_cidr_is_supported(self):
        request = self.resolve(HTTP_CF_CONNECTING_IP=CLIENT)
        self.assertEqual(request.META["REMOTE_ADDR"], CLIENT)

    @override_settings(TRUSTED_PROXY_IPS=[])
    def test_inactive_without_configuration(self):
        with self.assertRaises(MiddlewareNotUsed):
            TrustedProxyClientIPMiddleware(lambda _request: HttpResponse())

    @override_settings(TRUSTED_PROXY_IPS=["not-an-ip"])
    def test_invalid_configuration_fails_at_startup(self):
        with self.assertRaises(ImproperlyConfigured):
            TrustedProxyClientIPMiddleware(lambda _request: HttpResponse())
