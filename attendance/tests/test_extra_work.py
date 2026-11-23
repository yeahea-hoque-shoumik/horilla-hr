"""Holiday and day-off clock-in, clock-out and the extra work request."""

from datetime import date, datetime, time, timedelta
from datetime import timezone as dt_timezone
from unittest import mock

from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from attendance.methods.extra_work import (
    credit_days,
    full_shift_seconds,
    is_extra_work_day,
    resolve_shift_day,
)
from attendance.methods.utils import Request, strtime_seconds
from attendance.models import (
    Attendance,
    AttendanceActivity,
    AttendanceGeneralSetting,
    AttendanceOverTime,
    WorkRecords,
)
from attendance.scheduler import auto_punch_out
from attendance.views.clock_in_out import (
    clock_in,
    clock_in_attendance_and_activity,
    clock_out,
    clock_out_attendance_and_activity,
)
from base.models import (
    CompanyLeaves,
    Department,
    EmployeeShift,
    EmployeeShiftDay,
    EmployeeShiftSchedule,
    Holidays,
    Roster,
)
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_employee
from leave.models import CompensatoryLeaveRequest, LeaveGeneralSetting, LeaveType

MONDAY = date(2026, 11, 16)
SATURDAY = date(2026, 11, 14)
SUNDAY = date(2026, 11, 15)
# 04:00 UTC is 10:00 in Dhaka.
MONDAY_10AM_UTC = datetime(2026, 11, 16, 4, 0, tzinfo=dt_timezone.utc)
EIGHT_HOURS = 8 * 3600


class CreditDaysTests(SimpleTestCase):
    def test_boundaries(self):
        cases = [
            (EIGHT_HOURS, 1.0),
            (EIGHT_HOURS + 60, 1.0),
            (EIGHT_HOURS - 60, 0.5),
            (EIGHT_HOURS // 2 + 60, 0.5),
            (EIGHT_HOURS // 2, 0.0),
            (60, 0.0),
            (0, 0.0),
        ]
        for worked, expected in cases:
            with self.subTest(worked=worked):
                self.assertEqual(credit_days(worked, EIGHT_HOURS), expected)


class ExtraWorkBase(TestCase):
    def setUp(self):
        set_selected_company(None)
        self.days = {
            name: EmployeeShiftDay.objects.get_or_create(day=name)[0]
            for name in (
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            )
        }
        self.company = make_company("Extra Co")
        self.shift = EmployeeShift.objects.create(employee_shift="Day")
        for name in ("monday", "tuesday", "wednesday", "thursday", "friday"):
            EmployeeShiftSchedule.objects.create(
                day=self.days[name],
                shift_id=self.shift,
                minimum_working_hour="08:00",
                start_time=time(9),
                end_time=time(17),
            )
        self.employee = make_employee(
            company=self.company, email="extra@test.horilla", shift=self.shift
        )
        self.user = self.employee.employee_user_id
        self.user.is_new_employee = False
        self.user.save(update_fields=["is_new_employee"])
        LeaveGeneralSetting.objects.create(
            company_id=self.company, compensatory_leave=True
        )
        LeaveType.objects.create(
            name="Compensatory",
            is_compensatory_leave=True,
            payment="paid",
            company_id=self.company,
        )
        weekly_off = CompanyLeaves.objects.create(
            based_on_week=None, based_on_week_day="6"
        )
        weekly_off.company_id.add(self.company)

    def tearDown(self):
        set_selected_company(None)

    def punch(self, on_date, hours, minutes=0):
        clock_in_at = timezone.make_aware(datetime.combine(on_date, time(9)))
        clock_in_attendance_and_activity(
            employee=self.employee,
            date_today=on_date,
            attendance_date=on_date,
            day=self.days[on_date.strftime("%A").lower()],
            now="09:00",
            shift=self.shift,
            minimum_hour="08:00",
            start_time=strtime_seconds("09:00"),
            end_time=strtime_seconds("17:00"),
            in_datetime=clock_in_at,
        )
        clock_out_at = clock_in_at + timedelta(hours=hours, minutes=minutes)
        return clock_out_attendance_and_activity(
            employee=self.employee,
            date_today=on_date,
            now=clock_out_at.strftime("%H:%M"),
            out_datetime=clock_out_at,
        )

    def request_for(self, attendance):
        return CompensatoryLeaveRequest.objects.entire().get(
            source="extra_work", attendance_id=attendance
        )


class DayDetectionTests(ExtraWorkBase):
    def test_holiday_weekly_off_and_working_day(self):
        Holidays.objects.create(
            name="Bank", start_date=MONDAY, end_date=MONDAY, company_id=self.company
        )
        self.assertTrue(is_extra_work_day(self.employee, MONDAY))
        self.assertTrue(is_extra_work_day(self.employee, SUNDAY))
        self.assertFalse(is_extra_work_day(self.employee, MONDAY + timedelta(days=1)))

    def test_other_company_weekly_off_does_not_apply(self):
        other = make_company("Other Co", hq=False)
        weekly_off = CompanyLeaves.objects.create(
            based_on_week=None, based_on_week_day="2"
        )
        weekly_off.company_id.add(other)
        wednesday = MONDAY + timedelta(days=2)
        self.assertFalse(is_extra_work_day(self.employee, wednesday))

    def test_roster_overrides_company_weekly_off(self):
        department = Department.objects.create(department="Ops")
        Roster.objects.create(
            employee=self.employee, date=SUNDAY, department=department, is_off=False
        )
        Roster.objects.create(
            employee=self.employee, date=MONDAY, department=department, is_off=True
        )
        self.assertFalse(is_extra_work_day(self.employee, SUNDAY))
        self.assertTrue(is_extra_work_day(self.employee, MONDAY))


class ShiftResolutionTests(ExtraWorkBase):
    def test_unscheduled_day_uses_most_common_hours(self):
        attendance = self.punch(SUNDAY, 1)
        self.assertEqual(full_shift_seconds(attendance), EIGHT_HOURS)

    def test_no_schedule_falls_back_to_eight_hours(self):
        EmployeeShiftSchedule.objects.all().delete()
        attendance = self.punch(SUNDAY, 1)
        self.assertEqual(full_shift_seconds(attendance), EIGHT_HOURS)

    def _night_shift(self):
        night = EmployeeShift.objects.create(employee_shift="Night")
        EmployeeShiftSchedule.objects.create(
            day=self.days["friday"],
            shift_id=night,
            minimum_working_hour="08:00",
            start_time=time(22),
            end_time=time(6),
        )
        return night

    def test_after_midnight_punch_stays_on_friday_night_shift(self):
        result = resolve_shift_day(
            self._night_shift(), SATURDAY, strtime_seconds("01:00")
        )
        self.assertEqual(result[0], SATURDAY - timedelta(days=1))

    def test_saturday_morning_after_shift_end_is_saturday(self):
        result = resolve_shift_day(
            self._night_shift(), SATURDAY, strtime_seconds("10:00")
        )
        self.assertEqual(result[0], SATURDAY)


class ClockOutCreatesRequestTests(ExtraWorkBase):
    def test_full_shift_earns_one_day_and_stays_unvalidated(self):
        attendance = self.punch(SUNDAY, 8)
        self.assertTrue(attendance.is_extra_work)
        self.assertFalse(attendance.attendance_validated)
        self.assertEqual(attendance.overtime_second, 0)
        request = self.request_for(attendance)
        self.assertEqual(request.status, "requested")
        self.assertEqual(request.requested_days, 1.0)
        self.assertEqual(request.worked_seconds, EIGHT_HOURS)

    def test_more_than_half_earns_half_day(self):
        self.assertEqual(
            self.request_for(self.punch(SUNDAY, 4, 1)).requested_days, 0.5
        )

    def test_half_or_less_goes_to_hr_with_zero_days(self):
        request = self.request_for(self.punch(SUNDAY, 4))
        self.assertEqual(request.requested_days, 0.0)
        self.assertEqual(request.status, "requested")

    def test_second_session_updates_the_pending_request(self):
        self.punch(SUNDAY, 3)
        clock_in_at = timezone.make_aware(datetime.combine(SUNDAY, time(13)))
        clock_in_attendance_and_activity(
            employee=self.employee,
            date_today=SUNDAY,
            attendance_date=SUNDAY,
            day=self.days["sunday"],
            now="13:00",
            shift=self.shift,
            minimum_hour="08:00",
            start_time=strtime_seconds("09:00"),
            end_time=strtime_seconds("17:00"),
            in_datetime=clock_in_at,
        )
        clock_out_at = clock_in_at + timedelta(hours=5)
        attendance = clock_out_attendance_and_activity(
            employee=self.employee,
            date_today=SUNDAY,
            now=clock_out_at.strftime("%H:%M"),
            out_datetime=clock_out_at,
        )
        self.assertEqual(
            CompensatoryLeaveRequest.objects.entire()
            .filter(source="extra_work")
            .count(),
            1,
        )
        self.assertEqual(self.request_for(attendance).requested_days, 1.0)

    def test_working_day_is_unchanged(self):
        attendance = self.punch(MONDAY, 8)
        self.assertFalse(attendance.is_extra_work)
        self.assertFalse(
            CompensatoryLeaveRequest.objects.entire()
            .filter(attendance_id=attendance)
            .exists()
        )

    def test_flow_is_off_when_compensatory_leave_is_disabled(self):
        LeaveGeneralSetting.objects.update(compensatory_leave=False)
        attendance = self.punch(SUNDAY, 8)
        self.assertFalse(attendance.is_extra_work)

    def test_direct_validation_is_ignored(self):
        attendance = self.punch(SUNDAY, 8)
        attendance.attendance_validated = True
        attendance.save()
        attendance.refresh_from_db()
        self.assertFalse(attendance.attendance_validated)
        self.assertEqual(
            WorkRecords.objects.get(
                employee_id=self.employee, date=SUNDAY
            ).work_record_type,
            "CONF",
        )

    def test_device_punches_create_a_request_without_prompt(self):
        clock_in_at = timezone.make_aware(datetime.combine(SUNDAY, time(9)))
        clock_out_at = clock_in_at + timedelta(hours=8)
        clock_in(
            Request(
                user=self.user, date=SUNDAY, time=time(9), datetime=clock_in_at
            )
        )
        clock_out(
            Request(
                user=self.user, date=SUNDAY, time=time(17), datetime=clock_out_at
            )
        )
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertTrue(attendance.is_extra_work)
        self.assertEqual(self.request_for(attendance).requested_days, 1.0)

    def test_auto_punch_out_creates_a_request(self):
        EmployeeShiftSchedule.objects.create(
            day=self.days["sunday"],
            shift_id=self.shift,
            minimum_working_hour="08:00",
            start_time=time(9),
            end_time=time(17),
            is_auto_punch_out_enabled=True,
            auto_punch_out_time=time(17),
        )
        clock_in_attendance_and_activity(
            employee=self.employee,
            date_today=SUNDAY,
            attendance_date=SUNDAY,
            day=self.days["sunday"],
            now="09:00",
            shift=self.shift,
            minimum_hour="08:00",
            start_time=strtime_seconds("09:00"),
            end_time=strtime_seconds("17:00"),
            in_datetime=timezone.make_aware(datetime.combine(SUNDAY, time(9))),
        )
        auto_punch_out()
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertIsNotNone(attendance.attendance_clock_out)
        self.assertEqual(self.request_for(attendance).status, "requested")

    def test_pending_extra_work_is_not_hours_to_validate(self):
        attendance = self.punch(SUNDAY, 8)
        account = AttendanceOverTime.objects.get(
            employee_id=self.employee, month="november", year=SUNDAY.year
        )
        self.assertEqual(account.not_validated_hrs(), "00:00")
        self.assertTrue(attendance.is_extra_work)


@override_settings(TIME_ZONE="Asia/Dhaka")
class ClockInConfirmationTests(ExtraWorkBase):
    def setUp(self):
        super().setUp()
        AttendanceGeneralSetting.objects.create(company_id=None, enable_check_in=True)
        Holidays.objects.create(
            name="Bank", start_date=MONDAY, end_date=MONDAY, company_id=self.company
        )

    def _web_clock_in(self, confirm=False):
        client = Client()
        data = {"work_from": self.company.default_work_from_id}
        if confirm:
            data["confirm_extra_work"] = MONDAY.isoformat()
        with mock.patch("django.utils.timezone.now", return_value=MONDAY_10AM_UTC):
            client.force_login(self.user)
            return client.post(reverse("clock-in"), data, HTTP_HX_REQUEST="true")

    def test_first_punch_shows_notice_and_creates_nothing(self):
        response = self._web_clock_in()
        self.assertContains(response, "clockExtraWorkNotice")
        self.assertContains(response, MONDAY.isoformat())
        self.assertFalse(Attendance.objects.filter(employee_id=self.employee).exists())

    def test_confirmation_clocks_in(self):
        response = self._web_clock_in(confirm=True)
        self.assertNotContains(response, "clockExtraWorkNotice")
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertTrue(attendance.is_extra_work)

    def test_modal_shows_day_off_notice_before_submit(self):
        client = Client()
        with mock.patch("django.utils.timezone.now", return_value=MONDAY_10AM_UTC):
            client.force_login(self.user)
            response = client.get(reverse("clock-modal"), HTTP_HX_REQUEST="true")
        self.assertContains(response, "clockExtraWorkNotice")
        self.assertFalse(Attendance.objects.filter(employee_id=self.employee).exists())

    def test_working_day_has_no_notice(self):
        Holidays.objects.all().delete()
        response = self._web_clock_in()
        self.assertNotContains(response, "clockExtraWorkNotice")
        self.assertTrue(Attendance.objects.filter(employee_id=self.employee).exists())

    def test_repeat_punch_has_no_notice(self):
        self._web_clock_in(confirm=True)
        AttendanceActivity.objects.filter(employee_id=self.employee).update(
            clock_out=time(0, 1),
            clock_out_date=MONDAY - timedelta(days=1),
        )
        Attendance.objects.filter(employee_id=self.employee).update(
            attendance_clock_out=time(11),
            attendance_clock_out_date=MONDAY,
        )
        response = self._web_clock_in()
        self.assertNotContains(response, "clockExtraWorkNotice")

    def test_mobile_punch_has_no_prompt_and_creates_request(self):
        client = APIClient()
        client.force_authenticate(self.user)
        with mock.patch("django.utils.timezone.now", return_value=MONDAY_10AM_UTC):
            response = client.post(reverse("api-check-in"))
        self.assertEqual(response.status_code, 200, response.content)
        attendance = Attendance.objects.get(employee_id=self.employee)
        self.assertTrue(attendance.is_extra_work)
        later = MONDAY_10AM_UTC + timedelta(hours=8)
        # check_online() reads the real date, not the mocked punch date.
        with mock.patch("django.utils.timezone.now", return_value=later), mock.patch(
            "employee.models.Employee.check_online", return_value=True
        ):
            response = client.post(reverse("api-check-out"))
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.request_for(attendance).requested_days, 1.0)
