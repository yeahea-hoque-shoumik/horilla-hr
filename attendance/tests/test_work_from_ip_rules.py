"""IP restriction per company and work from pair, on web and mobile API."""

from datetime import timedelta, timezone as dt_timezone
from unittest import mock

from django.contrib.auth.models import Permission
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from attendance.methods.utils import Request
from attendance.tests.test_clock_modal import (
    INSTANT,
    TODAY,
    ClockModalBase,
    at,
)
from attendance.views.clock_in_out import clock_in
from base.forms import AttendanceWorkFromIPRuleForm
from base.models import AttendanceAllowedIP, AttendanceWorkFromIPRule, WorkFromRequest

OFFICE_IP = "203.0.113.10"
HOME_IP = "198.51.100.20"
COMPANY_IP = "192.0.2.30"


@override_settings(
    AXES_IPWARE_PROXY_COUNT=None, AXES_IPWARE_META_PRECEDENCE_ORDER=["REMOTE_ADDR"]
)
class IPRuleBase(ClockModalBase):
    def setUp(self):
        super().setUp()
        self.office = self.company.default_work_from
        self.restriction = AttendanceAllowedIP.objects.create(
            company_id=self.company,
            is_enabled=True,
            additional_data={"allowed_ips": [f"{COMPANY_IP}/32"]},
        )

    def rule(self, work_from=None, ips=(OFFICE_IP,), restricted=True, company=None):
        return AttendanceWorkFromIPRule.objects.create(
            company_id=company or self.company,
            work_from_id=work_from or self.office,
            is_restricted=restricted,
            allowed_ips=list(ips),
        )

    def approved_home(self):
        home = self.work_from("Home")
        WorkFromRequest.objects.bulk_create(
            [
                WorkFromRequest(
                    employee_id=self.employee,
                    work_from_id=home,
                    requested_date=TODAY,
                    requested_till=TODAY,
                    description="test",
                    approved=True,
                )
            ]
        )
        return home

    def web(self, url_name, ip, data=None, now=INSTANT):
        self.client.defaults["REMOTE_ADDR"] = ip
        return self.post(url_name, data or at(10), now=now)

    def api(self, url_name, ip, data=None, now=INSTANT):
        client = APIClient()
        client.force_authenticate(type(self.user).objects.get(pk=self.user.pk))
        with mock.patch("django.utils.timezone.now", return_value=now):
            return client.post(
                reverse(url_name), data or {}, format="json", REMOTE_ADDR=ip
            )


class WebCheckInTests(IPRuleBase):
    def test_pair_rule_allows_matching_ip(self):
        self.rule()
        self.web("clock-in", OFFICE_IP)
        self.assertEqual(self.activities().count(), 1)

    def test_pair_rule_replaces_company_list(self):
        self.rule()
        response = self.web("clock-in", COMPANY_IP)
        self.assertContains(response, "Check-In Restricted")
        self.assertFalse(self.activities().exists())

    def test_cidr_and_ipv6_entries_match(self):
        self.rule(ips=["203.0.113.0/24", "2404:1c40::/32"])
        self.web("clock-in", "2404:1c40:1cf:6606:84:5aa7:d5ab:ab82")
        self.assertEqual(self.activities().count(), 1)

    def test_unrestricted_rule_allows_any_network(self):
        home = self.approved_home()
        self.rule(work_from=home, ips=[], restricted=False)
        self.web("clock-in", HOME_IP, at(10, work_from=home.pk))
        self.assertEqual(self.activities().get().work_from_id, home)

    def test_no_rule_uses_company_list(self):
        self.assertContains(self.web("clock-in", HOME_IP), "Check-In Restricted")
        self.web("clock-in", COMPANY_IP)
        self.assertEqual(self.activities().count(), 1)

    def test_restricted_rule_without_ips_denies(self):
        self.rule(ips=[])
        self.assertContains(self.web("clock-in", COMPANY_IP), "Check-In Restricted")

    def test_disabled_restriction_ignores_rules(self):
        self.rule()
        AttendanceAllowedIP.objects.filter(pk=self.restriction.pk).update(
            is_enabled=False
        )
        self.web("clock-in", HOME_IP)
        self.assertEqual(self.activities().count(), 1)

    def test_other_company_rule_does_not_apply(self):
        self.rule(company=self.other_company, ips=[HOME_IP])
        self.assertContains(self.web("clock-in", HOME_IP), "Check-In Restricted")

    def test_session_company_cannot_avoid_restriction(self):
        session = self.client.session
        session["selected_company"] = str(self.other_company.pk)
        session.save()
        self.assertContains(self.web("clock-in", HOME_IP), "Check-In Restricted")
        self.assertFalse(self.activities().exists())

    def test_device_punch_stays_exempt(self):
        self.rule()
        moment = INSTANT.astimezone(dt_timezone(timedelta(hours=6)))
        clock_in(
            Request(
                user=self.user,
                date=moment.date(),
                time=moment.time(),
                datetime=moment,
            )
        )
        self.assertEqual(self.activities().count(), 1)


class WebCheckOutTests(IPRuleBase):
    def test_uses_work_from_saved_at_check_in(self):
        home = self.approved_home()
        self.rule(work_from=home, ips=[HOME_IP])
        self.rule(ips=[OFFICE_IP])
        self.web("clock-in", HOME_IP, at(10, work_from=home.pk))
        later = INSTANT + timedelta(hours=1)

        response = self.web("clock-out", OFFICE_IP, at(11), now=later)
        self.assertContains(response, "Check-Out Restricted")
        self.assertIsNone(self.activities().get().clock_out)

        self.web("clock-out", HOME_IP, at(11), now=later)
        self.assertIsNotNone(self.activities().get().clock_out)


class ApiTests(IPRuleBase):
    def test_check_in_blocked_with_403(self):
        self.rule()
        response = self.api("api-check-in", HOME_IP)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["error"],
            "Check-In Restricted: Your current network is not authorized",
        )
        self.assertFalse(self.activities().exists())

    def test_check_in_allowed(self):
        self.rule()
        response = self.api("api-check-in", OFFICE_IP)
        self.assertEqual(response.status_code, 200, response.content)

    def test_check_in_uses_selected_work_from_rule(self):
        home = self.approved_home()
        self.rule(work_from=home, ips=[], restricted=False)
        response = self.api("api-check-in", HOME_IP, {"work_from": home.pk})
        self.assertEqual(response.status_code, 200, response.content)

    def test_check_in_falls_back_to_company_list(self):
        self.assertEqual(self.api("api-check-in", HOME_IP).status_code, 403)
        self.assertEqual(self.api("api-check-in", COMPANY_IP).status_code, 200)

    def test_check_out_blocked_then_allowed(self):
        self.rule()
        self.assertEqual(self.api("api-check-in", OFFICE_IP).status_code, 200)
        later = INSTANT + timedelta(hours=1)

        # check_online() reads the real clock, not the mocked punch date.
        with mock.patch("employee.models.Employee.check_online", return_value=True):
            response = self.api("api-check-out", HOME_IP, now=later)
            self.assertEqual(response.status_code, 403)
            self.assertIsNone(self.activities().get().clock_out)

            response = self.api("api-check-out", OFFICE_IP, now=later)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIsNotNone(self.activities().get().clock_out)


class SettingsTests(IPRuleBase):
    def setUp(self):
        super().setUp()
        self.user.user_permissions.add(
            *Permission.objects.filter(
                codename__in=[
                    "add_attendance",
                    "change_attendance",
                    "delete_attendance",
                ]
            )
        )
        session = self.client.session
        session["selected_company"] = str(self.company.pk)
        session.save()

    def edit_url(self, work_from=None):
        return reverse("work-from-ip-rule-edit", args=[(work_from or self.office).pk])

    def save(self, data, work_from=None):
        return self.client.post(
            self.edit_url(work_from), data, HTTP_HX_REQUEST="true"
        )

    def test_list_shows_company_options_only(self):
        self.work_from("Foreign", company=self.other_company)
        response = self.client.get(
            reverse("work-from-ip-rules"), HTTP_HX_REQUEST="true"
        )
        self.assertContains(response, self.office.work_from)
        self.assertNotContains(response, "Foreign")

    def test_save_parses_and_dedupes_ips(self):
        self.save(
            {
                "is_restricted": "on",
                "ip_addresses": "203.0.113.0/24, 198.51.100.1\n203.0.113.0/24",
            }
        )
        rule = AttendanceWorkFromIPRule.objects.get(work_from_id=self.office)
        self.assertEqual(rule.allowed_ips, ["203.0.113.0/24", "198.51.100.1"])

    def test_update_keeps_one_row(self):
        self.rule()
        self.save({"ip_addresses": ""})
        rule = AttendanceWorkFromIPRule.objects.get(work_from_id=self.office)
        self.assertFalse(rule.is_restricted)

    def test_invalid_ip_is_rejected(self):
        response = self.save({"is_restricted": "on", "ip_addresses": "not-an-ip"})
        self.assertContains(response, "not a valid IP")
        self.assertNotContains(response, "Add at least one IP")
        self.assertFalse(AttendanceWorkFromIPRule.objects.exists())

    def test_restricted_needs_an_ip(self):
        response = self.save({"is_restricted": "on", "ip_addresses": ""})
        self.assertContains(response, "Add at least one IP")
        self.assertFalse(AttendanceWorkFromIPRule.objects.exists())

    def test_other_company_option_is_404(self):
        foreign = self.work_from("Foreign", company=self.other_company)
        response = self.save(
            {"is_restricted": "on", "ip_addresses": OFFICE_IP}, foreign
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_returns_to_company_list(self):
        self.rule()
        self.client.post(
            reverse("work-from-ip-rule-delete", args=[self.office.pk])
        )
        self.assertFalse(AttendanceWorkFromIPRule.objects.exists())

    def test_form_prefills_existing_ips(self):
        rule = self.rule(ips=[OFFICE_IP, HOME_IP])
        form = AttendanceWorkFromIPRuleForm(instance=rule)
        self.assertEqual(form["ip_addresses"].value(), f"{OFFICE_IP}\n{HOME_IP}")
