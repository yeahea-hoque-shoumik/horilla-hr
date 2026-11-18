"""
Clock-in/out took the attendance date and "HH:MM" from date.today() /
datetime.now(), which follow the container's OS timezone, while the activity
datetime came from timezone.localtime() (settings.TIME_ZONE). With the OS on
UTC and TIME_ZONE ahead of it, a punch just after local midnight landed on the
previous day. The views now derive all three from one timezone.localtime().

The instant used below is 2026-11-18 20:30 UTC == 2026-11-19 02:30 in Dhaka,
so a date taken from anything but TIME_ZONE shows up as the wrong day.
"""

from datetime import date, datetime, time, timezone as dt_timezone
from unittest import mock

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from attendance.models import Attendance, AttendanceActivity, AttendanceGeneralSetting
from base.models import EmployeeShiftDay
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_employee

INSTANT_UTC = datetime(2026, 11, 18, 20, 30, tzinfo=dt_timezone.utc)
LOCAL_DATE = date(2026, 11, 19)
LOCAL_TIME = time(2, 30)


def _messages(response):
    from django.contrib.messages import get_messages

    return [str(m) for m in get_messages(response.wsgi_request)]


@override_settings(TIME_ZONE="Asia/Dhaka")
class ClockInUsesSettingsTimezoneTests(TestCase):
    def setUp(self):
        set_selected_company(None)
        for day in (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ):
            EmployeeShiftDay.objects.get_or_create(day=day)
        self.company = make_company("TZ Co")
        self.employee = make_employee(company=self.company, email="tz@example.com")
        self.user = self.employee.employee_user_id
        # New employees are bounced to change-password by middleware.
        self.user.is_new_employee = False
        self.user.save(update_fields=["is_new_employee"])

    def _assert_punch_is_local(self):
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.attendance_date, LOCAL_DATE)
        self.assertEqual(attendance.attendance_clock_in_date, LOCAL_DATE)
        self.assertEqual(attendance.attendance_clock_in, LOCAL_TIME)
        activity = AttendanceActivity.objects.get(employee_id=self.employee)
        self.assertEqual(activity.attendance_date, LOCAL_DATE)
        self.assertEqual(activity.clock_in_date, LOCAL_DATE)

    def test_web_clock_in_dates_the_punch_in_settings_timezone(self):
        AttendanceGeneralSetting.objects.create(company_id=None, enable_check_in=True)
        client = Client()
        # Log in under the mocked clock: a session created at real time looks
        # expired once now() jumps to INSTANT_UTC.
        with mock.patch("django.utils.timezone.now", return_value=INSTANT_UTC):
            client.force_login(self.user)
            response = client.get(reverse("clock-in"), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200, _messages(response))
        self._assert_punch_is_local()

    def test_api_clock_in_dates_the_punch_in_settings_timezone(self):
        client = APIClient()
        client.force_authenticate(self.user)
        with mock.patch("django.utils.timezone.now", return_value=INSTANT_UTC):
            response = client.post(reverse("api-check-in"))
        self.assertEqual(response.status_code, 200, response.content)
        self._assert_punch_is_local()


@override_settings(TIME_ZONE="Asia/Dhaka")
class ClockInUsesEmployeeTimezoneTests(ClockInUsesSettingsTimezoneTests):
    """
    Same instant (20:30 UTC). An employee zone beats the company zone, which
    beats TIME_ZONE; each moves the stored local date/time accordingly.
    """

    def _set_zones(self, employee_tz=None, company_tz=None):
        from base.models import Company
        from employee.models import EmployeeWorkInformation

        Company.objects.filter(pk=self.company.pk).update(timezone=company_tz)
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            timezone=employee_tz
        )

    def _punch_api(self):
        client = APIClient()
        client.force_authenticate(self.user)
        with mock.patch("django.utils.timezone.now", return_value=INSTANT_UTC):
            response = client.post(reverse("api-check-in"))
        self.assertEqual(response.status_code, 200, response.content)
        return Attendance.objects.get(employee_id=self.employee)

    def test_employee_zone_overrides_company_and_settings(self):
        # 20:30 UTC == 20:30 in London (GMT in November), still Nov 18.
        self._set_zones(employee_tz="Europe/London", company_tz="Asia/Tokyo")
        attendance = self._punch_api()
        self.assertEqual(attendance.attendance_date, date(2026, 11, 18))
        self.assertEqual(attendance.attendance_clock_in, time(20, 30))

    def test_skipped_employee_zone_falls_back_to_company(self):
        # 20:30 UTC == 05:30 next day in Tokyo.
        self._set_zones(employee_tz=None, company_tz="Asia/Tokyo")
        attendance = self._punch_api()
        self.assertEqual(attendance.attendance_date, date(2026, 11, 19))
        self.assertEqual(attendance.attendance_clock_in, time(5, 30))

    def test_web_clock_in_uses_employee_zone(self):
        self._set_zones(employee_tz="Europe/London")
        AttendanceGeneralSetting.objects.create(company_id=None, enable_check_in=True)
        client = Client()
        # Log in under the mocked clock: a session created at real time looks
        # expired once now() jumps to INSTANT_UTC.
        with mock.patch("django.utils.timezone.now", return_value=INSTANT_UTC):
            client.force_login(self.user)
            response = client.get(reverse("clock-in"), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200, _messages(response))
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.attendance_date, date(2026, 11, 18))
        self.assertEqual(attendance.attendance_clock_in, time(20, 30))
