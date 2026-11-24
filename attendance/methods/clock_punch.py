"""
Rules for a punch submitted from the web check-in/check-out modal.

Times are chosen on the employee's current local date, in their own timezone,
and then follow the same storage path as an automatic punch.
"""

import ipaddress
from datetime import datetime, timedelta

from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

CHECK_IN_NETWORK_ERROR = gettext_lazy(
    "Check-In Restricted: Your current network is not authorized "
)
CHECK_OUT_NETWORK_ERROR = gettext_lazy(
    "Check-Out Restricted: Your current network is not authorized"
)


class PunchError(Exception):
    """A submitted punch that cannot be saved; the message is shown in the modal."""


def _company(employee):
    work_info = getattr(employee, "employee_work_info", None)
    return work_info.company_id if work_info else None


def work_froms_for_company(company):
    """Active work from options of a company, including all-company options."""
    from base.models import WorkFrom

    if company is None:
        return WorkFrom.objects.none()
    return (
        WorkFrom.objects.entire()
        .filter(Q(company_id=company) | Q(company_id__isnull=True), is_active=True)
        .distinct()
        .order_by("work_from")
    )


def available_work_froms(employee):
    """Options of the employee's own company, not the session's."""
    return work_froms_for_company(_company(employee))


def resolve_work_from(employee, raw_id):
    """Required when the company has work from options; must be one of that list."""
    if employee is None:
        return None
    work_froms = available_work_froms(employee)
    if not work_froms.exists():
        return None
    if not raw_id:
        raise PunchError(_("Please select your work location."))
    try:
        work_from = work_froms.filter(pk=int(raw_id)).first()
    except (TypeError, ValueError):
        work_from = None
    if work_from is None:
        raise PunchError(_("The selected work location is not available."))
    return work_from


def effective_work_from(employee):
    """The employee's own default if usable, otherwise their company's."""
    work_info = getattr(employee, "employee_work_info", None)
    company = _company(employee)
    if company is None:
        return None
    work_froms = available_work_froms(employee)
    for pk in (work_info.work_from_id_id, company.default_work_from_id):
        work_from = work_froms.filter(pk=pk).first() if pk else None
        if work_from:
            return work_from
    return None


def has_approved_work_from_request(employee, work_from, on_date):
    """True when an approved request for this option covers the given day."""
    from base.models import WorkFromRequest

    return (
        WorkFromRequest.objects.entire()
        .filter(
            employee_id=employee,
            work_from_id=work_from,
            approved=True,
            canceled=False,
            is_active=True,
            requested_date__lte=on_date,
        )
        .filter(Q(requested_till__gte=on_date) | Q(is_permanent_work_from=True))
        .exists()
    )


def ensure_work_from_allowed(employee, work_from, on_date):
    """Anything but the effective default needs an approved request."""
    if work_from is None:
        return
    default = effective_work_from(employee)
    if default and default.pk == work_from.pk:
        return
    if not has_approved_work_from_request(employee, work_from, on_date):
        raise PunchError(
            _("You are not allowed to work from %(work_from)s.")
            % {"work_from": work_from.work_from}
        )


def _ip_in_networks(ip, networks):
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for network in networks:
        try:
            if address in ipaddress.ip_network(network, strict=False):
                return True
        except (TypeError, ValueError):
            continue
    return False


def is_network_allowed(request, employee, work_from, fallback_company=None):
    """
    Check the caller's IP for this work from.

    The employee's company decides, so switching the session company cannot
    avoid a restriction. fallback_company only covers an employee without one.
    A pair rule wins; without one the company's allowed list applies.
    """
    from attendance.methods.utils import get_client_ip
    from base.models import AttendanceAllowedIP, AttendanceWorkFromIPRule

    company = _company(employee) or fallback_company
    # entire(): the default manager filters by the session's selected company.
    restriction = (
        AttendanceAllowedIP.objects.entire().filter(company_id=company).first()
    )
    if restriction is None or not restriction.is_enabled:
        return True

    rule = None
    if company is not None and work_from is not None:
        rule = (
            AttendanceWorkFromIPRule.objects.entire()
            .filter(company_id=company, work_from_id=work_from)
            .first()
        )
    if rule is None:
        allowed_ips = (restriction.additional_data or {}).get("allowed_ips", [])
    elif rule.is_restricted:
        allowed_ips = rule.allowed_ips or []
    else:
        return True
    return _ip_in_networks(get_client_ip(request), allowed_ips)


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
        .select_related("work_from_id")
        .order_by("attendance_date", "id")
        .last()
    )


def latest_open_activity(employee):
    """The activity clock-out will close, matching its own selection."""
    from attendance.models import AttendanceActivity

    return (
        AttendanceActivity.objects.filter(employee_id=employee, clock_out__isnull=True)
        .select_related("work_from_id")
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
