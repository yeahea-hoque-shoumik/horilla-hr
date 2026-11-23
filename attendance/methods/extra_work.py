"""
Extra work: holiday and day-off attendance that needs HR approval.

Every punch path (web, mobile, biometric, import, auto punch-out) can run
without a request, so these rules read the employee's own company instead of
the session's selected company.
"""

import logging
from collections import Counter
from datetime import timedelta

from django.apps import apps
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_noop

from attendance.methods.utils import shift_schedule_today, strtime_seconds

logger = logging.getLogger(__name__)

APPROVE_PERMISSION = "leave.change_compensatoryleaverequest"
DEFAULT_FULL_SHIFT_SECONDS = 8 * 60 * 60


class ExtraWorkError(Exception):
    """An extra-work decision that cannot be applied."""


def _company(employee):
    work_info = getattr(employee, "employee_work_info", None)
    return work_info.company_id if work_info else None


def extra_work_enabled(employee):
    """The flow follows the employee's company compensatory leave setting."""
    if not apps.is_installed("leave"):
        return False
    from leave.models import LeaveGeneralSetting

    settings_qs = LeaveGeneralSetting.objects.entire()
    company = _company(employee)
    setting = settings_qs.filter(company_id=company).first() if company else None
    setting = setting or settings_qs.filter(company_id__isnull=True).first()
    return bool(setting and setting.compensatory_leave)


def is_extra_work_day(employee, on_date):
    """
    True on a holiday, a roster day off, or a company weekly off. A roster
    entry for the date overrides the company weekly off.
    """
    from base.methods import is_company_leave, is_holiday
    from base.models import Roster

    company = _company(employee)
    if is_holiday(on_date, employee, company=company):
        return True
    roster = Roster.objects.entire().filter(employee=employee, date=on_date).first()
    if roster is not None:
        return roster.is_off
    return bool(is_company_leave(on_date, company=company))


def extra_work_applies(employee, on_date):
    return extra_work_enabled(employee) and is_extra_work_day(employee, on_date)


def needs_extra_work_confirmation(employee, on_date):
    """Only the first punch of a day off asks for confirmation."""
    from attendance.models import Attendance

    if Attendance._base_manager.filter(
        employee_id=employee, attendance_date=on_date
    ).exists():
        return False
    return extra_work_applies(employee, on_date)


def resolve_shift_day(shift, date_today, now_sec):
    """
    Return (attendance_date, day, minimum_hour, start_sec, end_sec) for a punch.

    Before noon a punch belongs to yesterday when today is a night shift. It
    also belongs to yesterday when today has no schedule and the punch falls
    inside yesterday's night shift, so a 1am punch from Friday's shift is not
    counted as Saturday extra work.
    """
    from base.models import EmployeeShiftDay

    def shift_day(for_date):
        return EmployeeShiftDay.objects.get(day=for_date.strftime("%A").lower())

    day = shift_day(date_today)
    minimum_hour, start_sec, end_sec = shift_schedule_today(day=day, shift=shift)
    if now_sec >= strtime_seconds("12:00"):
        return date_today, day, minimum_hour, start_sec, end_sec

    yesterday = date_today - timedelta(days=1)
    prev_day = shift_day(yesterday)
    prev_minimum, prev_start, prev_end = shift_schedule_today(day=prev_day, shift=shift)
    today_is_night = start_sec > end_sec
    today_unscheduled = not (start_sec or end_sec)
    inside_prev_night = prev_start > prev_end and now_sec <= prev_end
    if today_is_night or (today_unscheduled and inside_prev_night):
        return yesterday, prev_day, prev_minimum, prev_start, prev_end
    return date_today, day, minimum_hour, start_sec, end_sec


def full_shift_seconds(attendance):
    """That day's schedule, else the shift's most common daily hours, else 8h."""
    from base.models import EmployeeShiftSchedule

    schedules = EmployeeShiftSchedule._base_manager.filter(
        shift_id=attendance.shift_id
    )
    today = schedules.filter(day=attendance.attendance_day).first()
    if today and strtime_seconds(today.minimum_working_hour) > 0:
        return strtime_seconds(today.minimum_working_hour)
    hours = [
        seconds
        for seconds in (
            strtime_seconds(value)
            for value in schedules.values_list("minimum_working_hour", flat=True)
        )
        if seconds > 0
    ]
    if not hours:
        return DEFAULT_FULL_SHIFT_SECONDS
    # Ties go to the longer day so a rare short day can't lower the bar.
    return max(Counter(hours).items(), key=lambda item: (item[1], item[0]))[0]


def credit_days(worked_seconds, full_seconds):
    if worked_seconds >= full_seconds:
        return 1.0
    if worked_seconds * 2 > full_seconds:
        return 0.5
    return 0.0


def compensatory_leave_type_for(employee):
    """The employee's company type, else the shared one; created if missing."""
    from leave.models import LeaveType

    types = LeaveType.objects.entire().filter(is_compensatory_leave=True)
    company = _company(employee)
    leave_type = types.filter(company_id=company).first() if company else None
    leave_type = leave_type or types.filter(company_id__isnull=True).first()
    if leave_type:
        return leave_type
    return LeaveType.objects.create(
        name="Compensatory Leave Type",
        payment="paid",
        is_compensatory_leave=True,
        company_id=company,
    )


def _request_for(attendance, lock=False):
    from leave.models import CompensatoryLeaveRequest

    requests = CompensatoryLeaveRequest._base_manager.filter(
        source="extra_work", attendance_id=attendance
    )
    if lock:
        requests = requests.select_for_update()
    return requests.first()


def _attendance_of(comp_request):
    from attendance.models import Attendance

    return Attendance._base_manager.filter(
        compensatoryleaverequest=comp_request
    ).first()


def sync_extra_work_request(attendance):
    """
    Create or refresh the request at clock-out. A decided request is left
    alone, so later punches never change an approved credit.
    """
    from attendance.models import Attendance
    from leave.models import CompensatoryLeaveRequest

    if not attendance.is_extra_work or not attendance.attendance_clock_out:
        return None

    employee = attendance.employee_id
    worked = strtime_seconds(attendance.attendance_worked_hour)
    full = full_shift_seconds(attendance)
    days = credit_days(worked, full)

    with transaction.atomic():
        # Serialises concurrent clock-outs so a day gets a single request.
        Attendance._base_manager.select_for_update().filter(pk=attendance.pk).first()
        comp_request = _request_for(attendance, lock=True)
        if comp_request:
            if comp_request.status == "requested":
                comp_request.worked_seconds = worked
                comp_request.full_shift_seconds = full
                comp_request.requested_days = days
                comp_request.save()
            return comp_request

        comp_request = CompensatoryLeaveRequest.objects.create(
            leave_type_id=compensatory_leave_type_for(employee),
            employee_id=employee,
            requested_days=days,
            requested_date=attendance.attendance_date,
            description=f"Extra work on {attendance.attendance_date}",
            source="extra_work",
            worked_seconds=worked,
            full_shift_seconds=full,
        )
        comp_request.attendance_id.add(attendance)
        transaction.on_commit(lambda: _notify_hr(comp_request))
    return comp_request


def _notify_hr(comp_request):
    """A failed notification must never fail the employee's clock-out."""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Permission
    from notifications.signals import notify

    from base.auth_backends import company_scoped_active

    try:
        employee = comp_request.employee_id
        permission = Permission.objects.get(
            content_type__app_label="leave", codename="change_compensatoryleaverequest"
        )
        company = _company(employee)
        if company_scoped_active():
            group_grant = Q(
                company_group_assignments__company_id=getattr(company, "pk", None),
                company_group_assignments__group__permissions=permission,
            )
        else:
            group_grant = Q(groups__permissions=permission)
        recipients = (
            get_user_model()
            .objects.filter(
                Q(is_superuser=True) | Q(user_permissions=permission) | group_grant,
                is_active=True,
                employee_get__employee_work_info__company_id=company,
            )
            .exclude(pk=employee.employee_user_id_id)
            .distinct()
        )
        if recipients:
            notify.send(
                employee,
                recipient=recipients,
                verb=gettext_noop("%(employee)s submitted an extra work request"),
                verb_params={"employee": str(employee)},
                redirect=reverse("view-compensatory-leave")
                + f"?id={comp_request.id}",
                icon="time-outline",
            )
    except Exception:
        logger.exception("Extra work notification failed")


def can_decide_extra_work(user, comp_request):
    """HR admins only; reporting-manager access does not apply."""
    if not user.has_perm(APPROVE_PERMISSION):
        return False, _("Only HR admins can decide extra work requests.")
    if not user.is_superuser:
        employee = getattr(user, "employee_get", None)
        if employee and employee.pk == comp_request.employee_id_id:
            return False, _("You cannot decide your own extra work request.")
    return True, ""


def approve_extra_work(comp_request, user):
    """Validate the attendance and add the earned days, exactly once."""
    from leave.models import CompensatoryLeaveRequest

    allowed, error = can_decide_extra_work(user, comp_request)
    if not allowed:
        raise ExtraWorkError(error)

    with transaction.atomic():
        locked = CompensatoryLeaveRequest._base_manager.select_for_update().get(
            pk=comp_request.pk
        )
        if locked.status != "requested":
            raise ExtraWorkError(_("This extra work request is already decided."))
        attendance = _attendance_of(locked)
        if attendance is None:
            raise ExtraWorkError(_("The attendance for this request was not found."))
        # HR may have corrected the hours since clock-out.
        locked.worked_seconds = strtime_seconds(attendance.attendance_worked_hour)
        locked.full_shift_seconds = full_shift_seconds(attendance)
        locked.requested_days = credit_days(
            locked.worked_seconds, locked.full_shift_seconds
        )
        locked.status = "approved"
        locked.save()
        if locked.requested_days:
            locked.assign_compensatory_leave_type()
        attendance.attendance_validated = True
        attendance.approved_by = getattr(user, "employee_get", None)
        attendance.save()
    return locked


def reject_extra_work(comp_request, user, reason):
    """Reject a request; reversing an approval removes its unused days."""
    from leave.models import AvailableLeave, CompensatoryLeaveRequest

    allowed, error = can_decide_extra_work(user, comp_request)
    if not allowed:
        raise ExtraWorkError(error)

    with transaction.atomic():
        locked = CompensatoryLeaveRequest._base_manager.select_for_update().get(
            pk=comp_request.pk
        )
        if locked.status not in ("requested", "approved"):
            raise ExtraWorkError(_("This extra work request is already decided."))
        if locked.status == "approved" and locked.requested_days:
            balance = (
                AvailableLeave.objects.entire()
                .select_for_update()
                .filter(
                    employee_id=locked.employee_id,
                    leave_type_id=locked.leave_type_id,
                )
                .first()
            )
            remaining = (
                balance.available_days + balance.carryforward_days if balance else 0
            )
            if remaining < locked.requested_days:
                raise ExtraWorkError(
                    _("These extra work days are already used and cannot be removed.")
                )
            locked.exclude_compensatory_leave()
        locked.status = "rejected"
        locked.reject_reason = reason
        locked.save()
        attendance = _attendance_of(locked)
        if attendance is not None:
            attendance.attendance_validated = False
            attendance.save()
    return locked


def extra_work_record_status(attendance):
    """Return (work record type, message, day percentage) for an approved day."""
    comp_request = _request_for(attendance)
    days = comp_request.requested_days if comp_request else 0
    if days >= 1:
        return "FDP", _("Extra work: full day"), 1.0
    if days > 0:
        return "HDP", _("Extra work: half day"), 0.5
    return "HD", _("Extra work: no day earned"), 0.0
