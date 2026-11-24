"""Web check-in/check-out modal: chosen times, locations and geofencing."""

from datetime import date, datetime, time, timedelta, timezone as dt_timezone
from unittest import mock

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from attendance.methods.utils import Request
from attendance.models import (
    Attendance,
    AttendanceActivity,
    AttendanceGeneralSetting,
    AttendanceLateComeEarlyOut,
)
from attendance.views.clock_in_out import clock_in, clock_out
from base.models import (
    Company,
    EmployeeShift,
    EmployeeShiftDay,
    EmployeeShiftSchedule,
    WorkFrom,
    WorkFromRequest,
)
from employee.models import EmployeeWorkInformation
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_employee

# Wednesday 18 Nov 2026, 10:00 in Dhaka (UTC+6).
INSTANT = datetime(2026, 11, 18, 4, 0, tzinfo=dt_timezone.utc)
TODAY = date(2026, 11, 18)
INSIDE = {"latitude": "23.8103", "longitude": "90.4125"}
OUTSIDE = {"latitude": "22.3569", "longitude": "91.7832"}


def at(hour, minute="00", period="AM", **extra):
    return {
        "punch_hour": f"{hour:02d}",
        "punch_minute": minute,
        "punch_period": period,
        **extra,
    }


@override_settings(TIME_ZONE="Asia/Dhaka")
class ClockModalBase(TestCase):
    def setUp(self):
        set_selected_company(None)
        for name in ("monday", "tuesday", "wednesday", "thursday", "friday"):
            EmployeeShiftDay.objects.get_or_create(day=name)
        self.day = EmployeeShiftDay.objects.get(day="wednesday")
        self.company = make_company("Clock Co")
        self.other_company = make_company("Other Co")
        self.shift = EmployeeShift.objects.create(employee_shift="Day")
        EmployeeShiftSchedule.objects.create(
            day=self.day,
            shift_id=self.shift,
            minimum_working_hour="08:00",
            start_time=time(9),
            end_time=time(17),
        )
        self.employee = make_employee(
            company=self.company, email="clock@test.horilla", shift=self.shift
        )
        self.user = self.employee.employee_user_id
        self.user.is_new_employee = False
        self.user.save(update_fields=["is_new_employee"])
        AttendanceGeneralSetting.objects.create(company_id=None, enable_check_in=True)
        self.client = Client()
        # Real-time session: a session created at the mocked instant would
        # already be expired for requests that do not mock the clock.
        self.client.force_login(self.user)

    def tearDown(self):
        set_selected_company(None)

    def work_from(self, name="Office", company=None, **fields):
        company = company or self.company
        default = company.default_work_from
        if default.work_from == name and not fields:
            return default
        work_from = WorkFrom.objects.create(work_from=name, **fields)
        work_from.company_id.add(company)
        return work_from

    def get_modal(self, now=INSTANT):
        with mock.patch("django.utils.timezone.now", return_value=now):
            return self.client.get(reverse("clock-modal"), HTTP_HX_REQUEST="true")

    def post(self, url_name, data, now=INSTANT):
        if url_name == "clock-in" and "omit_work_from" not in data:
            data = {"work_from": self.company.default_work_from_id, **data}
        data = {key: value for key, value in data.items() if key != "omit_work_from"}
        with mock.patch("django.utils.timezone.now", return_value=now):
            return self.client.post(reverse(url_name), data, HTTP_HX_REQUEST="true")

    def activities(self):
        return AttendanceActivity.objects.filter(employee_id=self.employee)


class ModalDisplayTests(ClockModalBase):
    def test_shows_company_timezone_without_employee_zone(self):
        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Tokyo")
        response = self.get_modal()
        self.assertContains(response, 'data-timezone="Asia/Tokyo"')
        self.assertContains(response, '<option value="01" selected>01</option>')

    def test_employee_timezone_wins(self):
        Company.objects.filter(pk=self.company.pk).update(timezone="Asia/Tokyo")
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            timezone="Europe/London"
        )
        response = self.get_modal()
        self.assertContains(response, 'data-timezone="Europe/London"')
        self.assertContains(response, '<option value="04" selected>04</option>')

    def test_lists_only_active_locations_of_own_company(self):
        self.work_from("Head Office")
        self.work_from("Closed Branch", is_active=False)
        self.work_from("Other Office", company=self.other_company)
        response = self.get_modal()
        self.assertContains(response, "Head Office")
        self.assertNotContains(response, "Closed Branch")
        self.assertNotContains(response, "Other Office")

    def test_checkout_shows_check_in_and_no_location_field(self):
        place = self.work_from("Head Office")
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            work_from_id=place
        )
        self.post("clock-in", at(9, "15", work_from=place.pk))
        response = self.get_modal(INSTANT + timedelta(hours=1))
        self.assertContains(response, "clockCheckInSummary")
        self.assertContains(response, "09:15 AM")
        self.assertContains(response, "Head Office")
        self.assertNotContains(response, 'name="work_from"')


class PunchTimeTests(ClockModalBase):
    def test_get_never_punches(self):
        response = self.client.get(reverse("clock-in"), HTTP_HX_REQUEST="true")
        self.assertContains(response, "clockPunchModal")
        self.assertFalse(self.activities().exists())

    def test_chosen_time_is_saved_as_local_wall_time(self):
        response = self.post("clock-in", at(8, "45"))
        self.assertEqual(response["HX-Trigger"], "clockModalDone")
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.attendance_date, TODAY)
        self.assertEqual(attendance.attendance_clock_in, time(8, 45))
        activity = self.activities().get()
        self.assertEqual(activity.clock_in, time(8, 45))
        self.assertEqual(
            activity.in_datetime,
            datetime(2026, 11, 18, 2, 45, tzinfo=dt_timezone.utc),
        )

    def test_employee_zone_is_used_for_chosen_time(self):
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            timezone="Europe/London"
        )
        self.post("clock-in", at(3, "30"))
        activity = self.activities().get()
        self.assertEqual(activity.clock_in, time(3, 30))
        self.assertEqual(
            activity.in_datetime,
            datetime(2026, 11, 18, 3, 30, tzinfo=dt_timezone.utc),
        )

    def test_future_time_is_allowed(self):
        self.post("clock-in", at(11, "30"))
        self.assertEqual(self.activities().get().clock_in, time(11, 30))

    def test_invalid_time_creates_nothing(self):
        response = self.post("clock-in", at(13))
        self.assertContains(response, "valid time")
        self.assertEqual(response["HX-Retarget"], "#clockPunchModal")
        self.assertFalse(self.activities().exists())

    def test_late_mark_follows_chosen_time(self):
        with mock.patch(
            "attendance.views.clock_in_out.enable_late_come_early_out_tracking",
            return_value={"tracking": True},
        ):
            self.post("clock-in", at(8, "30"))
        self.assertFalse(
            AttendanceLateComeEarlyOut.objects.filter(
                employee_id=self.employee, type="late_come"
            ).exists()
        )

    def test_worked_hours_follow_chosen_times(self):
        self.post("clock-in", at(9))
        self.post("clock-out", at(5, "30", "PM"), INSTANT + timedelta(hours=8))
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.attendance_clock_out, time(17, 30))
        self.assertEqual(attendance.attendance_worked_hour, "08:30")
        self.assertEqual(attendance.attendance_overtime, "00:30")

    def test_checkout_before_check_in_is_rejected(self):
        self.post("clock-in", at(9))
        response = self.post("clock-out", at(8, "59"))
        self.assertContains(response, "before your check-in")
        self.assertIsNone(self.activities().get().clock_out)

    def test_repeat_check_in_before_last_checkout_is_rejected(self):
        self.post("clock-in", at(9))
        self.post("clock-out", at(10))
        response = self.post("clock-in", at(9, "30"))
        self.assertContains(response, "before your last check-out")
        self.assertEqual(self.activities().count(), 1)

    def test_night_shift_checkout_after_midnight(self):
        night = datetime(2026, 11, 18, 16, 0, tzinfo=dt_timezone.utc)  # 22:00
        self.post("clock-in", at(10, "00", "PM"), night)
        next_morning = night + timedelta(hours=8)  # 06:00 on the 19th
        self.post("clock-out", at(5, "45"), next_morning)
        activity = self.activities().get()
        self.assertEqual(activity.clock_out_date, date(2026, 11, 19))
        self.assertEqual(activity.clock_out, time(5, 45))
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.attendance_worked_hour, "07:45")


class WorkFromChoiceTests(ClockModalBase):
    def approve(self, work_from, start=TODAY, end=TODAY, **fields):
        fields.setdefault("approved", True)
        return WorkFromRequest.objects.bulk_create(
            [
                WorkFromRequest(
                    employee_id=self.employee,
                    work_from_id=work_from,
                    requested_date=start,
                    requested_till=end,
                    description="test",
                    **fields,
                )
            ]
        )[0]

    def set_employee_default(self, work_from):
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            work_from_id=work_from
        )

    def test_new_company_gets_required_default(self):
        default = self.company.default_work_from
        self.assertEqual(default.work_from, "Office")
        self.assertIn(self.company, default.company_id.all())

    def test_modal_preselects_company_default(self):
        response = self.get_modal()
        self.assertContains(
            response,
            f'value="{self.company.default_work_from_id}"\n'
            "                                    selected",
        )

    def test_modal_prefers_employee_default(self):
        home = self.work_from("Home")
        self.set_employee_default(home)
        response = self.get_modal()
        self.assertContains(
            response, f'value="{home.pk}"\n                                    selected'
        )

    def test_effective_default_needs_no_request(self):
        home = self.work_from("Home")
        self.set_employee_default(home)
        self.post("clock-in", at(9, work_from=home.pk))
        self.assertEqual(self.activities().get().work_from_id, home)

    def test_company_default_blocked_when_employee_has_own(self):
        self.set_employee_default(self.work_from("Home"))
        office = self.company.default_work_from
        response = self.post("clock-in", at(9, work_from=office.pk))
        self.assertContains(response, "You are not allowed to work from Office")
        self.assertFalse(self.activities().exists())

    def test_change_without_request_fails(self):
        home = self.work_from("Home")
        response = self.post("clock-in", at(9, work_from=home.pk))
        self.assertContains(response, "You are not allowed to work from Home")
        self.assertFalse(self.activities().exists())

    def test_unusable_requests_do_not_allow(self):
        home = self.work_from("Home")
        other = self.work_from("Ministry")
        yesterday = TODAY - timedelta(days=1)
        self.approve(home, approved=False)
        self.approve(home, canceled=True)
        self.approve(home, start=yesterday, end=yesterday)
        self.approve(other)
        response = self.post("clock-in", at(9, work_from=home.pk))
        self.assertContains(response, "You are not allowed to work from Home")
        self.assertFalse(self.activities().exists())

    def test_permanent_request_allows(self):
        home = self.work_from("Home")
        self.approve(
            home,
            start=TODAY - timedelta(days=30),
            end=None,
            is_permanent_work_from=True,
        )
        self.post("clock-in", at(9, work_from=home.pk))
        self.assertEqual(self.activities().get().work_from_id, home)

    def test_required_when_company_has_work_froms(self):
        response = self.post("clock-in", at(9, omit_work_from=True))
        self.assertContains(response, "select your work location")
        self.assertFalse(self.activities().exists())

    def test_saved_on_activity_and_attendance(self):
        place = self.work_from()
        self.post("clock-in", at(9, work_from=place.pk))
        self.assertEqual(self.activities().get().work_from_id, place)
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.work_from_id, place)

    def test_choice_overrides_employee_default(self):
        default = self.work_from("Office")
        home = self.work_from("Home")
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            work_from_id=default
        )
        self.approve(home)
        self.post("clock-in", at(9, work_from=home.pk))
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertEqual(attendance.work_from_id, home)

    def test_modal_lists_own_and_all_company_types_once(self):
        self.work_from("Ministry")
        WorkFrom.objects.create(work_from="Everywhere")
        self.work_from("Foreign Site", company=self.other_company)
        response = self.get_modal()
        self.assertContains(response, "Ministry", count=1)
        self.assertContains(response, "Everywhere", count=1)
        self.assertNotContains(response, "Foreign Site")

    def test_other_companys_work_from_is_rejected(self):
        self.work_from()
        foreign = self.work_from("Other", company=self.other_company)
        response = self.post("clock-in", at(9, work_from=foreign.pk))
        self.assertContains(response, "not available")
        self.assertFalse(self.activities().exists())

    def test_archived_work_from_is_rejected(self):
        self.work_from()
        closed = self.work_from("Closed", is_active=False)
        response = self.post("clock-in", at(9, work_from=closed.pk))
        self.assertContains(response, "not available")
        self.assertFalse(self.activities().exists())


class ApiWorkFromTests(ClockModalBase):
    def api_post(self, data=None):
        client = APIClient()
        # A fresh user, as on a real request: self.user caches its work info.
        client.force_authenticate(type(self.user).objects.get(pk=self.user.pk))
        with mock.patch("django.utils.timezone.now", return_value=INSTANT):
            return client.post(reverse("api-check-in"), data or {}, format="json")

    def approve(self, work_from):
        WorkFromRequest.objects.bulk_create(
            [
                WorkFromRequest(
                    employee_id=self.employee,
                    work_from_id=work_from,
                    requested_date=TODAY,
                    requested_till=TODAY,
                    description="test",
                    approved=True,
                )
            ]
        )

    def test_omitted_uses_company_default(self):
        response = self.api_post()
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(
            self.activities().get().work_from_id, self.company.default_work_from
        )

    def test_omitted_prefers_employee_default(self):
        home = self.work_from("Home")
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            work_from_id=home
        )
        self.assertEqual(self.api_post().status_code, 200)
        self.assertEqual(self.activities().get().work_from_id, home)

    def test_change_without_request_is_rejected(self):
        home = self.work_from("Home")
        response = self.api_post({"work_from": home.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "You are not allowed to work from Home."
        )
        self.assertFalse(self.activities().exists())

    def test_change_with_approved_request_is_saved(self):
        home = self.work_from("Home")
        self.approve(home)
        response = self.api_post({"work_from": home.pk})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.activities().get().work_from_id, home)

    def test_other_company_option_is_rejected(self):
        foreign = self.work_from("Foreign", company=self.other_company)
        self.approve(foreign)
        response = self.api_post({"work_from": foreign.pk})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.activities().exists())

    def test_invalid_value_is_rejected(self):
        response = self.api_post({"work_from": "abc"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.activities().exists())


class DevicePathTests(ClockModalBase):
    def test_device_punches_skip_modal_and_location(self):
        self.work_from()
        moment = INSTANT.astimezone(dt_timezone(timedelta(hours=6)))
        clock_in(
            Request(
                user=self.user, date=TODAY, time=time(10), datetime=moment
            )
        )
        activity = self.activities().get()
        self.assertIsNone(activity.work_from_id)
        later = moment + timedelta(hours=7)
        clock_out(
            Request(
                user=self.user, date=TODAY, time=time(17), datetime=later
            )
        )
        activity.refresh_from_db()
        self.assertEqual(activity.clock_out, time(17))
