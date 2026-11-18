"""Company.timezone: IANA zone dropdown, blank falls back to settings.TIME_ZONE."""

from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from base.forms import CompanyForm
from base.models import Company
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_user


class CompanyTimezoneFieldTests(TestCase):
    def setUp(self):
        set_selected_company(None)

    def test_model_rejects_unknown_zone(self):
        company = make_company("Bad TZ Co")
        company.timezone = "Mars/Olympus"
        with self.assertRaises(ValidationError) as ctx:
            company.full_clean()
        self.assertIn("timezone", ctx.exception.message_dict)

    @override_settings(TIME_ZONE="Asia/Kolkata")
    def test_get_timezone_falls_back_to_settings(self):
        company = make_company("No TZ Co")
        self.assertEqual(company.get_timezone(), ZoneInfo("Asia/Kolkata"))
        company.timezone = "Asia/Dhaka"
        self.assertEqual(company.get_timezone(), ZoneInfo("Asia/Dhaka"))

    def test_company_form_renders_a_dropdown_with_default_first(self):
        field = CompanyForm().fields["timezone"]
        values = [value for value, _ in field.choices]
        self.assertEqual(values[0], "")
        self.assertIn("Asia/Dhaka", values)
        self.assertIn('<select name="timezone"', str(CompanyForm()["timezone"]))


class SaveTimezoneViewTests(TestCase):
    def setUp(self):
        set_selected_company(None)
        self.company = make_company("Dhaka Co")
        self.other = make_company("Kolkata Co")
        # login_required also demands an Employee record for the user.
        from horilla.testkit import make_employee

        self.admin = make_user("tzadmin", is_superuser=True)
        make_employee(company=self.company, email="tzadmin@example.com", user=self.admin)
        self.client = Client()
        self.client.force_login(self.admin)
        session = self.client.session
        session["selected_company"] = str(self.company.pk)
        session.save()

    def _post(self, value):
        return self.client.post(reverse("save-timezone"), {"selected_timezone": value})

    def test_saves_zone_for_the_selected_company_only(self):
        self.assertEqual(self._post("Asia/Dhaka").status_code, 200)
        self.assertEqual(Company.objects.get(pk=self.company.pk).timezone, "Asia/Dhaka")
        self.assertIsNone(Company.objects.get(pk=self.other.pk).timezone)

    def test_blank_resets_to_default(self):
        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Dhaka")
        self.assertEqual(self._post("").status_code, 200)
        self.assertIsNone(Company.objects.get(pk=self.company.pk).timezone)

    def test_unknown_zone_is_rejected(self):
        self.assertEqual(self._post("Mars/Olympus").status_code, 400)
        self.assertIsNone(Company.objects.get(pk=self.company.pk).timezone)

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get(reverse("save-timezone")).status_code, 405)


@override_settings(TIME_ZONE="Asia/Kolkata")
class EmployeeTimezoneFallbackTests(TestCase):
    """Employee zone -> company zone -> settings.TIME_ZONE."""

    def setUp(self):
        set_selected_company(None)
        self.company = make_company("Fallback Co")

    def _employee(self, email):
        from horilla.testkit import make_employee

        return make_employee(company=self.company, email=email)

    def test_employee_zone_wins(self):
        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Dhaka")
        emp = self._employee("own@example.com")
        emp.employee_work_info.timezone = "Europe/London"
        self.assertEqual(emp.get_timezone(), ZoneInfo("Europe/London"))

    def test_skipped_employee_zone_uses_company_zone(self):
        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Dhaka")
        emp = self._employee("company@example.com")
        self.assertEqual(emp.get_timezone(), ZoneInfo("Asia/Dhaka"))

    def test_both_skipped_uses_settings(self):
        emp = self._employee("default@example.com")
        self.assertEqual(emp.get_timezone(), ZoneInfo("Asia/Kolkata"))

    def test_work_info_form_offers_company_default_first(self):
        from employee.forms import EmployeeWorkInformationForm

        choices = list(EmployeeWorkInformationForm().fields["timezone"].choices)
        self.assertEqual(choices[0][0], "")
        self.assertIn("Asia/Dhaka", [value for value, _ in choices])


@override_settings(TIME_ZONE="Asia/Kolkata")
class UserTimezoneMiddlewareTests(TestCase):
    """DB stays UTC; the active (display) zone follows the signed-in user."""

    def setUp(self):
        set_selected_company(None)
        self.company = make_company("Display Co")

    def _active_zone_for(self, user):
        from django.contrib.auth.models import AnonymousUser
        from django.test import RequestFactory
        from django.utils import timezone

        from base.middleware import UserTimezoneMiddleware

        seen = {}

        def get_response(request):
            seen["zone"] = timezone.get_current_timezone_name()
            return None

        request = RequestFactory().get("/")
        request.user = user or AnonymousUser()
        UserTimezoneMiddleware(get_response)(request)
        seen["after"] = timezone.get_current_timezone_name()
        return seen

    def test_employee_zone_is_active_during_the_request_and_reset_after(self):
        from horilla.testkit import make_employee

        emp = make_employee(company=self.company, email="mw@example.com")
        from employee.models import EmployeeWorkInformation

        EmployeeWorkInformation.objects.filter(employee_id=emp).update(
            timezone="Europe/London"
        )
        seen = self._active_zone_for(emp.employee_user_id)
        self.assertEqual(seen["zone"], "Europe/London")
        self.assertEqual(seen["after"], "Asia/Kolkata")

    def test_company_zone_when_employee_zone_skipped(self):
        from horilla.testkit import make_employee

        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Dhaka")
        emp = make_employee(company=self.company, email="mw2@example.com")
        self.assertEqual(self._active_zone_for(emp.employee_user_id)["zone"], "Asia/Dhaka")

    def test_anonymous_gets_settings_zone(self):
        self.assertEqual(self._active_zone_for(None)["zone"], "Asia/Kolkata")

    def test_datetimes_are_stored_in_utc_regardless_of_active_zone(self):
        from datetime import datetime, timezone as dt_tz

        from django.db import connection
        from django.utils import timezone

        with timezone.override(ZoneInfo("Europe/London")):
            company = make_company("UTC Check Co")
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT created_at FROM base_company WHERE id = %s", [company.pk]
            )
            raw = cursor.fetchone()[0]
        self.assertEqual(raw.utcoffset(), dt_tz.utc.utcoffset(datetime.now()))
