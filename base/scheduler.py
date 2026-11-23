import calendar
import logging
from datetime import date, datetime, timedelta

from django.db import IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_noop

from horilla.scheduling import register_job
from notifications.signals import notify

logger = logging.getLogger(__name__)


def update_rotating_work_from_assign(rotating_work_from, new_date):
    """
    Here will update the employee work information details and send notification
    """
    from horilla_auth.models import HorillaUser

    employee = rotating_work_from.employee_id
    employee_work_info = employee.employee_work_info
    work_from1 = rotating_work_from.rotating_work_from_id.work_from1
    work_from2 = rotating_work_from.rotating_work_from_id.work_from2
    additional_work_froms = (
        rotating_work_from.rotating_work_from_id.additional_work_froms()
    )
    if additional_work_froms is None:
        total_rotate_work_froms = [work_from1, work_from2]
    else:
        total_rotate_work_froms = [work_from1, work_from2] + list(additional_work_froms)
    next_work_from_index = rotating_work_from.additional_data.get(
        "next_work_from_index", 0
    )
    next_work_from = total_rotate_work_froms[next_work_from_index]
    if next_work_from_index < len(total_rotate_work_froms) - 1:
        next_work_from_index += 1
    else:
        next_work_from_index = 0

    rotating_work_from.additional_data["next_work_from_index"] = next_work_from_index
    employee_work_info.work_from_id = rotating_work_from.next_work_from
    employee_work_info.save()
    rotating_work_from.next_change_date = new_date
    rotating_work_from.current_work_from = rotating_work_from.next_work_from
    rotating_work_from.next_work_from = next_work_from
    rotating_work_from.save()
    bot = HorillaUser.objects.filter(username="Horilla Bot").first()
    if bot is not None:
        employee = rotating_work_from.employee_id
        notify.send(
            bot,
            recipient=employee.employee_user_id,
            verb=gettext_noop("Your Work From has been changed."),
            icon="infinite",
            redirect=reverse("employee-profile"),
        )
    return


def work_from_rotate_after(rotating_work_work_from):
    """
    This method for rotate work from based on after day
    """
    date_today = datetime.now()
    switch_date = rotating_work_work_from.next_change_date
    if switch_date.strftime("%Y-%m-%d") == date_today.strftime("%Y-%m-%d"):
        new_date = date_today + timedelta(days=rotating_work_work_from.rotate_after_day)
        update_rotating_work_from_assign(rotating_work_work_from, new_date)
    return


def work_from_rotate_weekend(rotating_work_from):
    """
    This method for rotate work from based on weekend
    """
    date_today = datetime.now()
    switch_date = rotating_work_from.next_change_date
    if switch_date.strftime("%Y-%m-%d") == date_today.strftime("%Y-%m-%d"):
        day = datetime.now().strftime("%A").lower()
        switch_day = rotating_work_from.rotate_every_weekend
        if day == switch_day:
            new_date = date_today + timedelta(days=7)
            update_rotating_work_from_assign(rotating_work_from, new_date)
    return


def work_from_rotate_every(rotating_work_from):
    """
    This method for rotate work from based on every month
    """
    date_today = datetime.now()
    switch_date = rotating_work_from.next_change_date
    day_date = rotating_work_from.rotate_every
    if switch_date.strftime("%Y-%m-%d") == date_today.strftime("%Y-%m-%d"):
        if day_date == switch_date.strftime("%d").lstrip("0"):
            new_date = date_today.replace(month=date_today.month + 1)
            update_rotating_work_from_assign(rotating_work_from, new_date)
        elif day_date == "last":
            year = date_today.strftime("%Y")
            month = date_today.strftime("%m")
            last_day = calendar.monthrange(int(year), int(month) + 1)[1]
            new_date = datetime(int(year), int(month) + 1, last_day)
            update_rotating_work_from_assign(rotating_work_from, new_date)
    return


def rotate_work_from():
    """
    This method will identify the based on condition to the rotating shift assign
    and redirect to the chunk method to execute.
    """
    from base.models import RotatingWorkFromAssign

    rotating_work_froms = RotatingWorkFromAssign.objects.filter(is_active=True)
    for rotating_work_from in rotating_work_froms:
        based_on = rotating_work_from.based_on
        if based_on == "after":
            work_from_rotate_after(rotating_work_from)
        elif based_on == "weekly":
            work_from_rotate_weekend(rotating_work_from)
        elif based_on == "monthly":
            work_from_rotate_every(rotating_work_from)
    return


def update_rotating_shift_assign(rotating_shift, new_date):
    """
    Here will update the employee work information and send notification
    """
    from horilla_auth.models import HorillaUser

    next_shift_index = 0
    employee = rotating_shift.employee_id
    employee_work_info = employee.employee_work_info
    rotating_shift_id = rotating_shift.rotating_shift_id
    shift1 = rotating_shift_id.shift1
    shift2 = rotating_shift_id.shift2
    additional_shifts = rotating_shift_id.additional_shifts()
    if additional_shifts is None:
        total_rotate_shifts = [shift1, shift2]
    else:
        total_rotate_shifts = [shift1, shift2] + list(additional_shifts)
    next_shift_index = rotating_shift.additional_data.get("next_shift_index")
    next_shift = total_rotate_shifts[next_shift_index]
    if next_shift_index < len(total_rotate_shifts) - 1:
        next_shift_index += 1
    else:
        next_shift_index = 0  # Wrap around to the beginning of the list
    rotating_shift.additional_data["next_shift_index"] = next_shift_index
    employee_work_info.shift_id = rotating_shift.next_shift
    employee_work_info.save()
    rotating_shift.next_change_date = new_date
    rotating_shift.current_shift = rotating_shift.next_shift
    rotating_shift.next_shift = next_shift
    rotating_shift.save()
    bot = HorillaUser.objects.filter(username="Horilla Bot").first()
    if bot is not None:
        employee = rotating_shift.employee_id
        notify.send(
            bot,
            recipient=employee.employee_user_id,
            verb=gettext_noop("Your shift has been changed."),
            icon="infinite",
            redirect=reverse("employee-profile"),
        )
    return


def shift_rotate_after_day(rotating_shift, today):
    """
    This method for rotate shift based on after day
    """
    switch_date = rotating_shift.next_change_date
    if switch_date == today:
        new_date = today + timedelta(days=rotating_shift.rotate_after_day)
        update_rotating_shift_assign(rotating_shift, new_date)
    return


def shift_rotate_weekend(rotating_shift, today):
    """
    This method for rotate shift based on weekend
    """
    switch_date = rotating_shift.next_change_date
    if switch_date == today:
        day = today.strftime("%A").lower()
        switch_day = rotating_shift.rotate_every_weekend
        if day == switch_day:
            new_date = today + timedelta(days=7)
            update_rotating_shift_assign(rotating_shift, new_date)
    return


def shift_rotate_every(rotating_shift, today):
    """
    This method for rotate shift based on every month
    """
    switch_date = rotating_shift.next_change_date
    day_date = rotating_shift.rotate_every
    if switch_date == today:
        if day_date == switch_date.strftime("%d").lstrip("0"):
            new_date = today.replace(month=today.month + 1)
            update_rotating_shift_assign(rotating_shift, new_date)
        elif day_date == "last":
            year = today.year
            month = today.month
            last_day = calendar.monthrange(int(year), int(month) + 1)[1]
            new_date = datetime(int(year), int(month) + 1, last_day)
            update_rotating_shift_assign(rotating_shift, new_date)
    return


def rotate_shift():
    """
    This method will identify the based on condition to the rotating shift assign
    and redirect to the chunk method to execute.
    """
    from base.models import RotatingShiftAssign

    rotating_shifts = RotatingShiftAssign.objects.filter(is_active=True)
    today = datetime.now().date()
    r_shifts = rotating_shifts.filter(start_date__lte=today)
    for r_shift in r_shifts:
        emp_shift = rotating_shifts.filter(
            employee_id=r_shift.employee_id, start_date__lte=today
        ).exclude(id=r_shift.id)
        emp_shift.update(is_active=False)

    # Re-read the active assignments: the superseded ones were just
    # deactivated. (A variable only set inside the loop above left nothing to
    # iterate when no assignment had started, raising TypeError every run.)
    for rotating_shift in rotating_shifts:
        based_on = rotating_shift.based_on
        # after day condition
        if based_on == "after":
            shift_rotate_after_day(rotating_shift, today)
        # weekly condition
        elif based_on == "weekly":
            shift_rotate_weekend(rotating_shift, today)
        # monthly condition
        elif based_on == "monthly":
            shift_rotate_every(rotating_shift, today)

    return


def switch_shift():
    """
    This method change employees shift information regards to the shift request
    """
    from base.models import ShiftRequest
    from horilla_auth.models import HorillaUser

    today = date.today()

    shift_requests = ShiftRequest.objects.filter(
        canceled=False, approved=True, requested_date__exact=today, shift_changed=False
    )
    if shift_requests:
        for request in shift_requests:
            work_info = request.employee_id.employee_work_info
            # updating requested shift to the employee work information.
            work_info.shift_id = request.shift_id
            work_info.save()
            request.approved = True
            request.shift_changed = True
            request.save()
            bot = HorillaUser.objects.filter(username="Horilla Bot").first()
            if bot is not None:
                employee = request.employee_id
                notify.send(
                    bot,
                    recipient=employee.employee_user_id,
                    verb=gettext_noop("Shift Changes notification"),
                    icon="refresh",
                    redirect=reverse("employee-profile"),
                )
    return


def undo_shift():
    """
    This method undo previous employees shift information regards to the shift request
    """
    from base.models import ShiftRequest
    from horilla_auth.models import HorillaUser

    today = date.today()
    # here will get all the active shift requests
    shift_requests = ShiftRequest.objects.filter(
        canceled=False,
        approved=True,
        requested_till__lt=today,
        is_active=True,
        shift_changed=True,
    )
    if shift_requests:
        for request in shift_requests:
            work_info = request.employee_id.employee_work_info
            work_info.shift_id = request.previous_shift_id
            work_info.save()
            # making the instance in-active
            request.is_active = False
            request.save()
            bot = HorillaUser.objects.filter(username="Horilla Bot").first()
            if bot is not None:
                employee = request.employee_id
                notify.send(
                    bot,
                    recipient=employee.employee_user_id,
                    verb=gettext_noop(
                        "Shift changes notification, Requested date expired."
                    ),
                    icon="refresh",
                    redirect=reverse("employee-profile"),
                )
    return


def switch_work_from():
    """
    This method change employees work from information regards to the work from request
    """
    from base.models import WorkFromRequest
    from horilla_auth.models import HorillaUser

    today = date.today()
    work_from_requests = WorkFromRequest.objects.filter(
        canceled=False,
        approved=True,
        requested_date__exact=today,
        work_from_changed=False,
    )
    for request in work_from_requests:
        work_info = request.employee_id.employee_work_info
        # updating requested work from to the employee work information.
        work_info.work_from_id = request.work_from_id
        work_info.save()
        request.approved = True
        request.work_from_changed = True
        request.save()
        bot = HorillaUser.objects.filter(username="Horilla Bot").first()
        if bot is not None:
            employee = request.employee_id
            notify.send(
                bot,
                recipient=employee.employee_user_id,
                verb=gettext_noop("Work From Changes notification"),
                icon="swap-horizontal",
                redirect=reverse("employee-profile"),
            )
    return


def undo_work_from():
    """
    This method undo previous employees work from information regards to the work from request
    """
    from base.models import WorkFromRequest
    from horilla_auth.models import HorillaUser

    today = date.today()
    # here will get all the active work from requests
    work_from_requests = WorkFromRequest.objects.filter(
        canceled=False,
        approved=True,
        requested_till__lt=today,
        is_active=True,
        work_from_changed=True,
    )
    for request in work_from_requests:
        work_info = request.employee_id.employee_work_info
        # updating employee work information's work from to previous work from
        work_info.work_from_id = request.previous_work_from_id
        work_info.save()
        # making the instance is in-active
        request.is_active = False
        request.save()
        bot = HorillaUser.objects.filter(username="Horilla Bot").first()
        if bot is not None:
            employee = request.employee_id
            notify.send(
                bot,
                recipient=employee.employee_user_id,
                verb=gettext_noop(
                    "Work from changes notification, Requested date expired."
                ),
                icon="swap-horizontal",
                redirect=reverse("employee-profile"),
            )
    return


def recurring_holiday():
    from .models import Holidays

    recurring_holidays = Holidays.objects.filter(recurring=True)
    today = datetime.now()
    # Looping through all recurring holiday
    for recurring_holiday in recurring_holidays:
        start_date = recurring_holiday.start_date
        end_date = recurring_holiday.end_date
        new_start_date = date(start_date.year + 1, start_date.month, start_date.day)
        new_end_date = date(end_date.year + 1, end_date.month, end_date.day)
        # Checking that end date is not none
        if end_date is None:
            # checking if that start date is day before today
            if start_date == (today - timedelta(days=1)).date():
                recurring_holiday.start_date = new_start_date
        elif end_date == (today - timedelta(days=1)).date():
            recurring_holiday.start_date = new_start_date
            recurring_holiday.end_date = new_end_date
        try:
            recurring_holiday.save()
        except IntegrityError:
            # Another holiday already occupies the rolled-over date range
            # for this company; keep this one unchanged.
            logger.warning(
                "Recurring holiday %s not rolled over: duplicate date range",
                recurring_holiday.pk,
            )


def sync_roster_shifts():
    """
    Daily at 00:05 — sync published roster entries to employee work info.
    For each employee with a published non-off roster entry dated today,
    update their EmployeeWorkInformation.shift_id to match.
    """
    from base.models import Roster
    from employee.models import EmployeeWorkInformation

    today = date.today()
    entries = (
        Roster.objects.filter(date=today, is_published=True, is_off=False)
        .select_related("employee", "shift")
        .exclude(shift__isnull=True)
    )
    for entry in entries:
        try:
            work_info = EmployeeWorkInformation.objects.filter(
                employee_id=entry.employee
            ).first()
            if work_info and work_info.shift_id != entry.shift:
                work_info.shift_id = entry.shift
                work_info.save(update_fields=["shift_id"])
        except Exception:
            pass


# The job1..job6 ids are historical and deliberately preserved so existing
# jobstore rows are replaced rather than duplicated. Note job5/job6 are swapped
# relative to declaration order -- that is how they have always been persisted.
# These registrations were previously wrapped in bare `except: pass`, which made
# a failed registration indistinguishable from a working one.
register_job(rotate_shift, "interval", job_id="job1", hours=4)
register_job(rotate_work_from, "interval", job_id="job2", hours=4)
register_job(undo_shift, "interval", job_id="job3", hours=4)
register_job(switch_shift, "interval", job_id="job4", hours=4)
register_job(undo_work_from, "interval", job_id="job6", hours=4)
register_job(switch_work_from, "interval", job_id="job5", hours=4)
register_job(recurring_holiday, "interval", hours=4)
register_job(sync_roster_shifts, "interval", hours=4)
