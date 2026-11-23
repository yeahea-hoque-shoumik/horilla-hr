"""
clock_in_out.py

This module is used register endpoints to the check-in check-out functionalities
"""

import ipaddress
import logging

from django.shortcuts import render
from django.urls import reverse

from horilla.http.response import HorillaRedirect

logger = logging.getLogger(__name__)
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from attendance.methods.clock_punch import (
    PunchError,
    available_work_locations,
    current_open_activity,
    ensure_after_check_in,
    ensure_after_last_punch,
    latest_open_activity,
    parse_punch_time,
    resolve_work_location,
)
from attendance.methods.extra_work import (
    extra_work_applies,
    needs_extra_work_confirmation,
    resolve_shift_day,
    sync_extra_work_request,
)
from attendance.methods.utils import (
    activity_datetime,
    employee_exists,
    employee_localtime,
    format_time,
    geofence_denial_web,
    get_client_ip,
    overtime_calculation,
    shift_schedule_today,
    strtime_seconds,
)
from attendance.models import (
    Attendance,
    AttendanceActivity,
    AttendanceGeneralSetting,
    AttendanceLateComeEarlyOut,
    GraceTime,
)
from attendance.views.views import attendance_validate
from base.context_processors import (
    enable_late_come_early_out_tracking,
    timerunner_enabled,
)
from base.middleware import resolve_user_timezone
from base.models import AttendanceAllowedIP, Company, EmployeeShiftDay
from horilla.decorators import hx_request_required, login_required
from horilla.horilla_middlewares import _thread_locals


def late_come_create(attendance):
    """
    used to create late come report
    args:
        attendance : attendance object
    """

    if AttendanceLateComeEarlyOut.objects.filter(
        type="late_come", attendance_id=attendance
    ).exists():
        late_come_obj = AttendanceLateComeEarlyOut.objects.filter(
            type="late_come", attendance_id=attendance
        ).first()
    else:
        late_come_obj = AttendanceLateComeEarlyOut()

    late_come_obj.type = "late_come"
    late_come_obj.attendance_id = attendance
    late_come_obj.employee_id = attendance.employee_id
    late_come_obj.save()
    return late_come_obj


def late_come(attendance, start_time, end_time, shift):
    """
    this method is used to mark the late check-in  attendance after the shift starts
    args:
        attendance : attendance obj
        start_time : attendance day shift start time
        end_time : attendance day shift end time

    """
    if not shift:
        return
    if not enable_late_come_early_out_tracking(None).get("tracking"):
        return
    request = getattr(_thread_locals, "request", None)
    now_sec = strtime_seconds(attendance.attendance_clock_in.strftime("%H:%M"))
    mid_day_sec = strtime_seconds("12:00")

    # Checking gracetime allowance before creating late come
    if shift and shift.grace_time_id:
        # checking grace time in shift, it has the higher priority
        if (
            shift.grace_time_id.is_active == True
            and shift.grace_time_id.allowed_clock_in == True
        ):
            # Setting allowance for the check in time
            now_sec -= shift.grace_time_id.allowed_time_in_secs
    # checking default grace time
    elif GraceTime.objects.filter(is_default=True, is_active=True).exists():
        grace_time = GraceTime.objects.filter(
            is_default=True,
            is_active=True,
        ).first()
        # Setting allowance for the check in time if grace allocate for clock in event
        if grace_time.allowed_clock_in:
            now_sec -= grace_time.allowed_time_in_secs
    else:
        pass
    if start_time > end_time and start_time != end_time:
        # night shift
        if now_sec < mid_day_sec:
            # Here  attendance or attendance activity for new day night shift
            late_come_create(attendance)
        elif now_sec > start_time:
            # Here  attendance or attendance activity for previous day night shift
            late_come_create(attendance)
    elif start_time < now_sec:
        late_come_create(attendance)
    return True


def clock_in_attendance_and_activity(
    employee,
    date_today,
    attendance_date,
    day,
    now,
    shift,
    minimum_hour,
    start_time,
    end_time,
    in_datetime,
    work_location=None,
):
    """
    This method is used to create attendance activity or attendance when an employee clocks-in
    args:
        employee        : employee instance
        date_today      : date
        attendance_date : the date that attendance for
        day             : shift day
        now             : current time
        shift           : shift object
        minimum_hour    : minimum hour in shift schedule
        start_time      : start time in shift schedule
        end_time        : end time in shift schedule
    """

    # attendance activity create
    activity = AttendanceActivity.objects.filter(
        employee_id=employee,
        attendance_date=attendance_date,
        clock_in_date=date_today,
        shift_day=day,
        clock_out=None,
    ).first()

    if activity and not activity.clock_out:
        activity.clock_out = in_datetime
        activity.clock_out_date = date_today
        activity.save()

    new_activity = AttendanceActivity.objects.create(
        employee_id=employee,
        attendance_date=attendance_date,
        clock_in_date=date_today,
        shift_day=day,
        clock_in=in_datetime,
        in_datetime=in_datetime,
        work_location=work_location,
    )
    # create attendance if not exist
    attendance = Attendance.objects.filter(
        employee_id=employee, attendance_date=attendance_date
    )
    if not attendance.exists():
        attendance = Attendance()
        attendance.employee_id = employee
        attendance.shift_id = shift
        attendance.work_type_id = attendance.employee_id.employee_work_info.work_type_id
        attendance.attendance_date = attendance_date
        attendance.attendance_day = day
        attendance.attendance_clock_in = now
        attendance.attendance_clock_in_date = date_today
        attendance.minimum_hour = minimum_hour
        attendance.work_location = work_location
        if extra_work_applies(employee, attendance_date):
            attendance.is_extra_work = True
            attendance.attendance_validated = False
            attendance.minimum_hour = "00:00"
        attendance.save()
        # check here late come or not

        attendance = Attendance.find(attendance.id)
        late_come(
            attendance=attendance, start_time=start_time, end_time=end_time, shift=shift
        )
    else:
        attendance = attendance[0]
        attendance.attendance_clock_out = None
        attendance.attendance_clock_out_date = None
        attendance.save()
        # delete if the attendance marked the early out
        early_out_instance = attendance.late_come_early_out.filter(type="early_out")
        if early_out_instance.exists():
            early_out_instance[0].delete()
    return attendance


def _session_company(request):
    selected_company = request.session.get("selected_company")
    if selected_company == "all":
        return None
    return Company.objects.filter(id=selected_company).first()


def _company_fence_on(company):
    from geofencing.models import GeoFencing

    if company is None:
        return False
    fence = GeoFencing.objects.filter(company_id=company).first()
    return bool(fence and fence.start)


def _render_clock_modal(request, error="", extra_work_date=None):
    """Render the modal. Submitted values are kept when it is shown again."""
    employee, work_info = employee_exists(request)
    if employee is None or work_info is None:
        messages.error(
            request,
            _(
                "Check-In Unavailable: Your employee profile or work information is incomplete."
            ),
        )
        return HorillaRedirect(request)

    local_now = employee_localtime(employee)
    activity = current_open_activity(employee, local_now)
    mode = "out" if activity else "in"
    company = _session_company(request)
    locations = list(available_work_locations(employee)) if mode == "in" else []

    if mode == "out":
        needs_geo = (
            activity.work_location.has_fence
            if activity.work_location
            else _company_fence_on(company)
        )
    else:
        needs_geo = not locations and _company_fence_on(company)
        if extra_work_date is None and not request.POST:
            attendance_date = resolve_shift_day(
                work_info.shift_id,
                local_now.date(),
                strtime_seconds(local_now.strftime("%H:%M")),
            )[0]
            if needs_extra_work_confirmation(employee, attendance_date):
                extra_work_date = attendance_date

    posted = request.POST if request.method == "POST" else {}
    time_edited = bool(posted.get("punch_hour"))
    context = {
        "mode": mode,
        "activity": activity,
        "locations": locations,
        "selected_location": posted.get("work_location", ""),
        "error": error,
        "extra_work_date": extra_work_date,
        "needs_geo": needs_geo,
        "local_now": local_now,
        "now_ms": int(local_now.timestamp() * 1000),
        "timezone_name": str(resolve_user_timezone(employee.employee_user_id)),
        "submit_url": reverse("clock-out" if mode == "out" else "clock-in"),
        "hour_options": [f"{hour:02d}" for hour in range(1, 13)],
        "minute_options": [f"{minute:02d}" for minute in range(60)],
        "selected_hour": posted.get("punch_hour") or local_now.strftime("%I"),
        "selected_minute": posted.get("punch_minute") or local_now.strftime("%M"),
        "selected_period": posted.get("punch_period") or local_now.strftime("%p"),
        "time_edited": time_edited,
    }
    response = render(request, "attendance/components/clock_modal.html", context)
    if request.method == "POST":
        # The form sits in the open modal; replace it instead of the button.
        response["HX-Retarget"] = "#clockPunchModal"
        response["HX-Reswap"] = "outerHTML"
    return response


def _punch_saved(request):
    """Refresh the top-bar button and close the modal."""
    response = render(
        request, "attendance/components/in_out_component.html", {"run": 1}
    )
    if not request.__dict__.get("datetime"):
        response["HX-Trigger"] = "clockModalDone"
    return response


@login_required
@hx_request_required
def clock_modal(request):
    """Check-in/check-out modal for the signed-in employee."""
    return _render_clock_modal(request)


@login_required
@hx_request_required
def clock_in(request):
    """
    This method is used to mark the attendance once per a day and multiple attendance activities.
    """
    # Device and import punches carry their own datetime and never see the modal.
    if not request.__dict__.get("datetime") and request.method != "POST":
        return _render_clock_modal(request)
    # check wether check in/check out feature is enabled
    selected_company = request.session.get("selected_company")
    if selected_company == "all":
        company = None
        attendance_general_settings = AttendanceGeneralSetting.objects.filter(
            company_id=None
        ).first()
    else:
        company = Company.objects.filter(id=selected_company).first()
        attendance_general_settings = AttendanceGeneralSetting.objects.filter(
            company_id=company
        ).first()
    # request.__dict__.get("datetime")' used to check if the request is from a biometric device
    if (
        attendance_general_settings
        and attendance_general_settings.enable_check_in
        or request.__dict__.get("datetime")
    ):
        allowed_attendance_ips = AttendanceAllowedIP.objects.filter(
            company_id=company
        ).first()

        if (
            not request.__dict__.get("datetime")
            and allowed_attendance_ips
            and allowed_attendance_ips.is_enabled
        ):
            # get_client_ip() only trusts X-Forwarded-For as far as the
            # deployment's declared proxy count -- taking the client-supplied
            # header at face value let anyone claim to be on the office
            # network.
            ip = get_client_ip(request)

            allowed_ips = (allowed_attendance_ips.additional_data or {}).get(
                "allowed_ips", []
            )
            ip_allowed = False
            for allowed_ip in allowed_ips:
                try:
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(
                        allowed_ip, strict=False
                    ):
                        ip_allowed = True
                        break
                except ValueError:
                    continue

            if not ip_allowed:
                return _render_clock_modal(
                    request,
                    error=_(
                        "Check-In Restricted: Your current network is not authorized "
                    ),
                )

        employee, work_info = employee_exists(request)
        work_location = None
        if not request.__dict__.get("datetime"):
            try:
                work_location = resolve_work_location(
                    employee, request.POST.get("work_location")
                )
            except PunchError as error:
                return _render_clock_modal(request, error=str(error))
            # The mobile/API clock-in already enforces a configured
            # geo-fence; this view didn't, so an employee outside the fence
            # could still punch in from a browser.
            geofence_error = geofence_denial_web(request, company, work_location)
            if geofence_error:
                return _render_clock_modal(request, error=geofence_error)

        # One clock read, in the employee's zone (own > company > TIME_ZONE),
        # for date, time and datetime. date.today()/datetime.now() follow the
        # container's OS timezone and could put the punch on the wrong day.
        local_now = employee_localtime(employee)
        if employee and not request.__dict__.get("datetime"):
            try:
                local_now = parse_punch_time(request.POST, local_now)
                ensure_after_last_punch(employee, local_now)
            except PunchError as error:
                return _render_clock_modal(request, error=str(error))
        datetime_now = local_now
        if request.__dict__.get("datetime"):
            datetime_now = request.datetime
        if employee and work_info is not None:
            shift = work_info.shift_id
            date_today = local_now.date()
            if request.__dict__.get("date"):
                date_today = request.date
            now = local_now.strftime("%H:%M")
            if request.__dict__.get("time"):
                now = request.time.strftime("%H:%M")
            now_sec = strtime_seconds(now)
            (
                attendance_date,
                day,
                minimum_hour,
                start_time_sec,
                end_time_sec,
            ) = resolve_shift_day(shift, date_today, now_sec)
            # Device and import punches carry their own datetime: no one to ask.
            if (
                not request.__dict__.get("datetime")
                and request.POST.get("confirm_extra_work")
                != attendance_date.isoformat()
                and needs_extra_work_confirmation(employee, attendance_date)
            ):
                return _render_clock_modal(request, extra_work_date=attendance_date)
            attendance = clock_in_attendance_and_activity(
                employee=employee,
                date_today=date_today,
                attendance_date=attendance_date,
                day=day,
                now=now,
                shift=shift,
                minimum_hour=minimum_hour,
                start_time=start_time_sec,
                end_time=end_time_sec,
                in_datetime=datetime_now,
                work_location=work_location,
            )
            # Refresh employee from DB so template re-evaluates is_clocked_in correctly
            employee.refresh_from_db()
            return _punch_saved(request)
        messages.error(
            request,
            _(
                "Check-In Unavailable: Your employee profile or work information is incomplete."
            ),
        )
        return HorillaRedirect(request)
    else:
        messages.error(
            request,
            _(
                "The attendance check-in/check-out feature has not been enabled for your company."
            ),
        )
        return HorillaRedirect(request)


def clock_out_attendance_and_activity(employee, date_today, now, out_datetime=None):
    """
    Clock out the attendance and activity
    args:
        employee    : employee instance
        date_today  : today date
        now         : now
    """

    attendance_activities = AttendanceActivity.objects.filter(
        employee_id=employee,
    ).order_by("attendance_date", "id")
    attendance_activity = None  # Initialize attendance_activity

    if attendance_activities.filter(clock_out__isnull=True).exists():
        attendance_activity = attendance_activities.filter(
            clock_out__isnull=True
        ).last()
        attendance_activity.clock_out = out_datetime
        attendance_activity.clock_out_date = date_today
        attendance_activity.out_datetime = out_datetime
        attendance_activity.save()

        attendance_activities = attendance_activities.filter(
            attendance_date=attendance_activity.attendance_date
        )
        # Here calculate the total durations between the attendance activities

        duration = 0
        for activity in attendance_activities:
            in_datetime, out_datetime = activity_datetime(activity)
            difference = out_datetime - in_datetime
            days_second = difference.days * 24 * 3600
            seconds = difference.seconds
            total_seconds = days_second + seconds
            duration = duration + total_seconds
        duration = format_time(duration)
        # update clock out of attendance
        attendance = Attendance.objects.filter(employee_id=employee).order_by(
            "-attendance_date", "-id"
        )[0]
        attendance.attendance_clock_out = now + ":00"
        attendance.attendance_clock_out_date = date_today
        attendance.attendance_worked_hour = duration
        # Overtime calculation
        attendance.attendance_overtime = overtime_calculation(attendance)

        # Validate the attendance as per the condition
        if attendance.is_extra_work:
            attendance.attendance_validated = attendance.extra_work_approved()
        else:
            attendance.attendance_validated = attendance_validate(attendance)
        attendance.save()
        sync_extra_work_request(attendance)

        return attendance

    logger.error("No attendance clock in activity found that needs clocking out.")
    return


def early_out_create(attendance):
    """
    Used to create early out report
    args:
        attendance : attendance obj
    """
    if AttendanceLateComeEarlyOut.objects.filter(
        type="early_out", attendance_id=attendance
    ).exists():
        late_come_obj = AttendanceLateComeEarlyOut.objects.filter(
            type="early_out", attendance_id=attendance
        ).first()
    else:
        late_come_obj = AttendanceLateComeEarlyOut()
    late_come_obj.type = "early_out"
    late_come_obj.attendance_id = attendance
    late_come_obj.employee_id = attendance.employee_id
    late_come_obj.save()
    return late_come_obj


def early_out(attendance, start_time, end_time, shift):
    """
    This method is used to mark the early check-out attendance before the shift ends
    args:
        attendance : attendance obj
        start_time : attendance day shift start time
        start_end : attendance day shift end time
    """
    if not shift:
        return
    if not enable_late_come_early_out_tracking(None).get("tracking"):
        return

    clock_out_time = attendance.attendance_clock_out
    if isinstance(clock_out_time, str):
        clock_out_time = datetime.strptime(clock_out_time, "%H:%M:%S")

    now_sec = strtime_seconds(clock_out_time.strftime("%H:%M"))
    mid_day_sec = strtime_seconds("12:00")
    # Checking gracetime allowance before creating early out
    if shift and shift.grace_time_id:
        if (
            shift.grace_time_id.is_active == True
            and shift.grace_time_id.allowed_clock_out == True
        ):
            now_sec += shift.grace_time_id.allowed_time_in_secs
    elif GraceTime.objects.filter(is_default=True, is_active=True).exists():
        grace_time = GraceTime.objects.filter(
            is_default=True,
            is_active=True,
        ).first()
        # Setting allowance for the check out time if grace allocate for clock out event
        if grace_time.allowed_clock_out:
            now_sec += grace_time.allowed_time_in_secs
    else:
        pass
    if start_time > end_time:
        # Early out condition for night shift
        if now_sec < mid_day_sec:
            if now_sec < end_time:
                # Early out condition for general shift
                early_out_create(attendance)
        else:
            early_out_create(attendance)
        return
    if end_time > now_sec:
        early_out_create(attendance)
    return


@login_required
@hx_request_required
def clock_out(request):
    """
    This method is used to set the out date and time for attendance and attendance activity
    """
    if not request.__dict__.get("datetime") and request.method != "POST":
        return _render_clock_modal(request)
    # check wether check in/check out feature is enabled
    selected_company = request.session.get("selected_company")
    if selected_company == "all":
        company = None
        attendance_general_settings = AttendanceGeneralSetting.objects.filter(
            company_id=None
        ).first()
    else:
        company = Company.objects.filter(id=selected_company).first()
        attendance_general_settings = AttendanceGeneralSetting.objects.filter(
            company_id=company
        ).first()
    if (
        attendance_general_settings
        and attendance_general_settings.enable_check_in
        or request.__dict__.get("datetime")
    ):
        allowed_attendance_ips = AttendanceAllowedIP.objects.filter(
            company_id=company
        ).first()

        if (
            not request.__dict__.get("datetime")
            and allowed_attendance_ips
            and allowed_attendance_ips.is_enabled
        ):
            # get_client_ip() only trusts X-Forwarded-For as far as the
            # deployment's declared proxy count -- taking the client-supplied
            # header at face value let anyone claim to be on the office
            # network.
            ip = get_client_ip(request)

            allowed_ips = (allowed_attendance_ips.additional_data or {}).get(
                "allowed_ips", []
            )
            ip_allowed = False
            for allowed_ip in allowed_ips:
                try:
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(
                        allowed_ip, strict=False
                    ):
                        ip_allowed = True
                        break
                except ValueError:
                    continue

            if not ip_allowed:
                return _render_clock_modal(
                    request,
                    error=_(
                        "Check-Out Restricted: Your current network is not authorized"
                    ),
                )

        # Same single clock read in the employee's zone as clock_in, so both
        # sides agree on the date the punch belongs to.
        employee, work_info = employee_exists(request)
        local_now = employee_localtime(employee)
        if not request.__dict__.get("datetime"):
            open_activity = latest_open_activity(employee)
            # Check-out has no location choice: the check-in's location applies.
            geofence_error = geofence_denial_web(
                request,
                company,
                open_activity.work_location if open_activity else None,
            )
            if geofence_error:
                return _render_clock_modal(request, error=geofence_error)
            try:
                local_now = parse_punch_time(request.POST, local_now)
                ensure_after_check_in(open_activity, local_now)
            except PunchError as error:
                return _render_clock_modal(request, error=str(error))
        datetime_now = local_now
        if request.__dict__.get("datetime"):
            datetime_now = request.datetime
        shift = work_info.shift_id
        date_today = local_now.date()
        if request.__dict__.get("date"):
            date_today = request.date
        day = date_today.strftime("%A").lower()
        day = EmployeeShiftDay.objects.get(day=day)
        attendance = (
            Attendance.objects.filter(employee_id=employee)
            .order_by("id", "attendance_date")
            .last()
        )
        if attendance is not None:
            if not attendance.attendance_day:
                day_name = attendance.attendance_date.strftime("%A").lower()
                attendance.attendance_day = EmployeeShiftDay.objects.get(day=day_name)
                attendance.save(update_fields=["attendance_day"])
            day = attendance.attendance_day
        now = local_now.strftime("%H:%M")
        if request.__dict__.get("time"):
            now = request.time.strftime("%H:%M")
        minimum_hour, start_time_sec, end_time_sec = shift_schedule_today(
            day=day, shift=shift
        )
        attendance = clock_out_attendance_and_activity(
            employee=employee, date_today=date_today, now=now, out_datetime=datetime_now
        )
        if attendance:
            early_out_instance = attendance.late_come_early_out.filter(type="early_out")
            is_night_shift = attendance.is_night_shift()
            next_date = attendance.attendance_date + timedelta(days=1)
            if not early_out_instance.exists():
                if is_night_shift:
                    now_sec = strtime_seconds(now)
                    mid_sec = strtime_seconds("12:00")

                    if (attendance.attendance_date == date_today) or (
                        # check is next day mid
                        mid_sec >= now_sec
                        and date_today == next_date
                    ):
                        early_out(
                            attendance=attendance,
                            start_time=start_time_sec,
                            end_time=end_time_sec,
                            shift=shift,
                        )
                elif attendance.attendance_date == date_today:
                    early_out(
                        attendance=attendance,
                        start_time=start_time_sec,
                        end_time=end_time_sec,
                        shift=shift,
                    )

        # Refresh employee from DB so template re-evaluates is_clocked_in correctly
        employee.refresh_from_db()
        return _punch_saved(request)

    else:
        messages.error(
            request,
            _(
                "The attendance check-in/check-out feature has not been enabled for your company."
            ),
        )
        return HorillaRedirect(request)
