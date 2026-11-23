"""HR decisions on extra work requests."""

from datetime import date, datetime, time, timedelta

from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from attendance.methods.extra_work import (
    ExtraWorkError,
    approve_extra_work,
    reject_extra_work,
)
from attendance.methods.utils import strtime_seconds
from attendance.models import Attendance, WorkRecords
from attendance.views.clock_in_out import (
    clock_in_attendance_and_activity,
    clock_out_attendance_and_activity,
)
from base.models import (
    CompanyLeaves,
    EmployeeShift,
    EmployeeShiftDay,
    EmployeeShiftSchedule,
)
from employee.models import EmployeeWorkInformation
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_employee
from leave.methods import get_leave_day_attendance
from leave.models import (
    AvailableLeave,
    CompensatoryLeaveRequest,
    LeaveGeneralSetting,
    LeaveType,
)

SUNDAY = date(2026, 11, 15)


class ExtraWorkApprovalTests(TestCase):
    def setUp(self):
        set_selected_company(None)
        self.monday = EmployeeShiftDay.objects.get_or_create(day="monday")[0]
        self.sunday = EmployeeShiftDay.objects.get_or_create(day="sunday")[0]
        self.company = make_company("Approve Co")
        self.shift = EmployeeShift.objects.create(employee_shift="Day")
        EmployeeShiftSchedule.objects.create(
            day=self.monday,
            shift_id=self.shift,
            minimum_working_hour="08:00",
            start_time=time(9),
            end_time=time(17),
        )
        self.employee = make_employee(
            company=self.company, email="worker@test.horilla", shift=self.shift
        )
        self.hr = make_employee(company=self.company, email="hr@test.horilla")
        self.manager = make_employee(company=self.company, email="mgr@test.horilla")
        EmployeeWorkInformation.objects.filter(employee_id=self.employee).update(
            reporting_manager_id=self.manager
        )
        self.permission = Permission.objects.get(
            content_type__app_label="leave",
            codename="change_compensatoryleaverequest",
        )
        self.hr_user = self.hr.employee_user_id
        self.hr_user.is_new_employee = False
        self.hr_user.save(update_fields=["is_new_employee"])
        self.hr_user.user_permissions.add(self.permission)
        LeaveGeneralSetting.objects.create(
            company_id=self.company, compensatory_leave=True
        )
        self.leave_type = LeaveType.objects.create(
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

    def _request(self, hours=8):
        clock_in_at = timezone.make_aware(datetime.combine(SUNDAY, time(9)))
        clock_in_attendance_and_activity(
            employee=self.employee,
            date_today=SUNDAY,
            attendance_date=SUNDAY,
            day=self.sunday,
            now="09:00",
            shift=self.shift,
            minimum_hour="00:00",
            start_time=strtime_seconds("09:00"),
            end_time=strtime_seconds("17:00"),
            in_datetime=clock_in_at,
        )
        clock_out_at = clock_in_at + timedelta(hours=hours)
        attendance = clock_out_attendance_and_activity(
            employee=self.employee,
            date_today=SUNDAY,
            now=clock_out_at.strftime("%H:%M"),
            out_datetime=clock_out_at,
        )
        request = CompensatoryLeaveRequest.objects.entire().get(
            source="extra_work", attendance_id=attendance
        )
        return request, attendance

    def _balance(self):
        row = AvailableLeave.objects.entire().filter(
            employee_id=self.employee, leave_type_id=self.leave_type
        )
        return row.first().available_days if row.exists() else 0

    def _record_type(self):
        return WorkRecords.objects.get(
            employee_id=self.employee, date=SUNDAY
        ).work_record_type

    def test_approval_validates_attendance_and_adds_days(self):
        request, attendance = self._request()
        approve_extra_work(request, self.hr_user)
        attendance.refresh_from_db()
        self.assertTrue(attendance.attendance_validated)
        self.assertEqual(attendance.overtime_second, 0)
        self.assertEqual(self._balance(), 1.0)
        self.assertEqual(self._record_type(), "FDP")

    def test_half_day_approval(self):
        request, _attendance = self._request(hours=5)
        approve_extra_work(request, self.hr_user)
        self.assertEqual(self._balance(), 0.5)
        self.assertEqual(self._record_type(), "HDP")

    def test_zero_day_approval_adds_attendance_only(self):
        request, attendance = self._request(hours=2)
        approve_extra_work(request, self.hr_user)
        attendance.refresh_from_db()
        self.assertTrue(attendance.attendance_validated)
        self.assertEqual(self._balance(), 0)
        self.assertEqual(self._record_type(), "HD")

    def test_double_approval_does_not_double_credit(self):
        request, _attendance = self._request()
        approve_extra_work(request, self.hr_user)
        with self.assertRaises(ExtraWorkError):
            approve_extra_work(request, self.hr_user)
        self.assertEqual(self._balance(), 1.0)

    def test_reporting_manager_without_permission_cannot_decide(self):
        request, attendance = self._request()
        with self.assertRaises(ExtraWorkError):
            approve_extra_work(request, self.manager.employee_user_id)
        attendance.refresh_from_db()
        self.assertFalse(attendance.attendance_validated)

    def test_hr_cannot_approve_own_request(self):
        self.employee.employee_user_id.user_permissions.add(self.permission)
        request, _attendance = self._request()
        employee_user = type(self.employee.employee_user_id).objects.get(
            pk=self.employee.employee_user_id_id
        )
        with self.assertRaises(ExtraWorkError):
            approve_extra_work(request, employee_user)
        self.assertEqual(self._balance(), 0)

    def test_rejection_leaves_attendance_unvalidated(self):
        request, attendance = self._request()
        reject_extra_work(request, self.hr_user, "Not requested")
        attendance.refresh_from_db()
        request.refresh_from_db()
        self.assertFalse(attendance.attendance_validated)
        self.assertEqual(request.status, "rejected")
        self.assertEqual(request.reject_reason, "Not requested")
        self.assertEqual(self._balance(), 0)

    def test_reversal_removes_days_and_unvalidates(self):
        request, attendance = self._request()
        approve_extra_work(request, self.hr_user)
        reject_extra_work(request, self.hr_user, "Mistake")
        attendance.refresh_from_db()
        self.assertFalse(attendance.attendance_validated)
        self.assertEqual(self._balance(), 0)

    def test_reversal_is_blocked_when_days_are_used(self):
        request, attendance = self._request()
        approve_extra_work(request, self.hr_user)
        AvailableLeave.objects.entire().filter(employee_id=self.employee).update(
            available_days=0, carryforward_days=0
        )
        with self.assertRaises(ExtraWorkError):
            reject_extra_work(request, self.hr_user, "Too late")
        attendance.refresh_from_db()
        self.assertTrue(attendance.attendance_validated)

    def test_reversal_takes_remainder_from_carryforward(self):
        request, _attendance = self._request()
        approve_extra_work(request, self.hr_user)
        AvailableLeave.objects.entire().filter(employee_id=self.employee).update(
            available_days=0.5, carryforward_days=2
        )
        reject_extra_work(request, self.hr_user, "Mistake")
        row = AvailableLeave.objects.entire().get(employee_id=self.employee)
        self.assertEqual(row.available_days, 0)
        self.assertEqual(row.carryforward_days, 1.5)

    def test_manual_comp_off_form_cannot_claim_extra_work(self):
        request, attendance = self._request()
        approve_extra_work(request, self.hr_user)
        self.assertNotIn(
            attendance, list(get_leave_day_attendance(self.employee))
        )

    def test_approval_uses_hours_corrected_by_hr(self):
        request, attendance = self._request(hours=8)
        attendance.attendance_worked_hour = "05:00"
        attendance.save()
        approved = approve_extra_work(request, self.hr_user)
        self.assertEqual(approved.requested_days, 0.5)
        self.assertEqual(self._balance(), 0.5)

    def test_attendance_request_approval_cannot_validate_extra_work(self):
        request, attendance = self._request()
        self.hr_user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="attendance", codename="change_attendance"
            )
        )
        client = Client()
        client.force_login(self.hr_user)
        client.post(
            reverse("approve-validate-attendance-request", args=[attendance.pk]),
            HTTP_HX_REQUEST="true",
        )
        attendance = Attendance.objects.entire().get(pk=attendance.pk)
        self.assertFalse(attendance.attendance_validated)
        request.refresh_from_db()
        self.assertEqual(request.status, "requested")

    def test_approval_through_the_view(self):
        request, attendance = self._request()
        client = Client()
        client.force_login(self.hr_user)
        response = client.post(
            reverse("approve-compensatory-leave", args=[request.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertLess(response.status_code, 400)
        attendance = Attendance.objects.entire().get(pk=attendance.pk)
        self.assertTrue(attendance.attendance_validated)
        self.assertEqual(self._balance(), 1.0)
