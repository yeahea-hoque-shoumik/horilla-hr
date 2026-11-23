"""
Rules for a punch submitted from the web check-in/check-out modal.

Times are chosen on the employee's current local date, in their own timezone,
and then follow the same storage path as an automatic punch.
"""

from datetime import datetime, timedelta

from django.utils.translation import gettext as _


class PunchError(Exception):
    """A submitted punch that cannot be saved; the message is shown in the modal."""


def _company(employee):
    work_info = getattr(employee, "employee_work_info", None)
    return work_info.company_id if work_info else None


def available_work_locations(employee):
    """Active locations of the employee's own company, not the session's."""
    from attendance.models import WorkLocation

    company = _company(employee)
    if company is None:
        return WorkLocation.objects.none()
    return (
        WorkLocation.objects.entire()
        .filter(company_id=company, is_active=True)
        .order_by("name")
    )


def resolve_work_location(employee, raw_id):
    """Required when the company has locations; must be one of that list."""
    if employee is None:
        return None
    locations = available_work_locations(employee)
    if not locations.exists():
        return None
    if not raw_id:
        raise PunchError(_("Please select your work location."))
    try:
        location = locations.filter(pk=int(raw_id)).first()
    except (TypeError, ValueError):
        location = None
    if location is None:
        raise PunchError(_("The selected work location is not available."))
    return location


def parse_punch_time(data, local_now):
    """
    Return an aware datetime on the employee's current date. An unchanged
    hour and minute keeps the exact current time.
    """
    hour, minute, period = (
        data.get("punch_hour"),
        data.get("punch_minute"),
        data.get("punch_period"),
    )
    if not (hour or minute or period):
        return local_now
    try:
        hour, minute = int(hour), int(minute)
    except (TypeError, ValueError) as error:
        raise PunchError(_("Please enter a valid time.")) from error
    period = (period or "").upper()
    if period not in ("AM", "PM") or not 1 <= hour <= 12 or not 0 <= minute <= 59:
        raise PunchError(_("Please enter a valid time."))
    hour = hour % 12 + (12 if period == "PM" else 0)
    if hour == local_now.hour and minute == local_now.minute:
        return local_now
    return local_now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def _minute(value):
    return value.replace(second=0, microsecond=0, tzinfo=None)


def current_open_activity(employee, local_now):
    """The open punch the top-bar button treats as checked in."""
    from attendance.models import AttendanceActivity

    today = local_now.date()
    return (
        AttendanceActivity.objects.filter(
            employee_id=employee,
            clock_out__isnull=True,
            attendance_date__in=[today - timedelta(days=1), today],
        )
        .select_related("work_location")
        .order_by("attendance_date", "id")
        .last()
    )


def latest_open_activity(employee):
    """The activity clock-out will close, matching its own selection."""
    from attendance.models import AttendanceActivity

    return (
        AttendanceActivity.objects.filter(employee_id=employee, clock_out__isnull=True)
        .select_related("work_location")
        .order_by("attendance_date", "id")
        .last()
    )


def ensure_after_last_punch(employee, punch_at):
    """A new check-in cannot start before the previous punch ended."""
    from attendance.models import AttendanceActivity

    activity = (
        AttendanceActivity.objects.filter(employee_id=employee)
        .order_by("-attendance_date", "-id")
        .first()
    )
    if activity is None:
        return
    if activity.clock_out and activity.clock_out_date:
        last = datetime.combine(activity.clock_out_date, activity.clock_out)
        error = _("Check-in time cannot be before your last check-out.")
    elif activity.clock_in_date and activity.clock_in:
        last = datetime.combine(activity.clock_in_date, activity.clock_in)
        error = _("Check-in time cannot be before your last check-in.")
    else:
        return
    if _minute(punch_at) < _minute(last):
        raise PunchError(error)


def ensure_after_check_in(activity, punch_at):
    """Check-out cannot be before the check-in it closes."""
    if activity is None or not activity.clock_in_date or not activity.clock_in:
        return
    checked_in = datetime.combine(activity.clock_in_date, activity.clock_in)
    if _minute(punch_at) < _minute(checked_in):
        raise PunchError(_("Check-out time cannot be before your check-in time."))
