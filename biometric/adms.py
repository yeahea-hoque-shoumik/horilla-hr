"""
Receiver for ZKTeco ADMS (PUSH protocol) devices such as the SenseFace 2A.

Push devices connect to Horilla instead of Horilla connecting to them:

1. ``GET  /iclock/cdata?SN=...``       handshake; the reply sets the device options.
2. ``POST /iclock/cdata?SN=...&table=ATTLOG``  attendance records, one per line.
3. ``GET  /iclock/getrequest?SN=...``  the device polls for commands.
4. ``POST /iclock/devicecmd?SN=...``   the device reports a command result.

A device is accepted only when its serial number belongs to an active push
device registered in Horilla, and, when that device lists source addresses
in Machine IP, only from those addresses. The PIN on the device is matched to
``Employee.badge_id`` within the device's company.
"""

import ipaddress
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from attendance.methods.clock_punch import latest_open_activity
from attendance.methods.utils import Request, get_client_ip
from attendance.views.clock_in_out import clock_in, clock_out
from employee.models import Employee

from .models import BiometricDevices, BiometricPushLog

logger = logging.getLogger(__name__)

# ZKTeco punch states: check-in, break-in, overtime-in / check-out, break-out,
# overtime-out. Anything else (255 on access-control firmware) has no meaning.
IN_STATUS_CODES = {0, 3, 4}
OUT_STATUS_CODES = {1, 2, 5}

LAST_SEEN_INTERVAL = timedelta(minutes=1)
UNKNOWN_DEVICE_LOG_SECONDS = 600
ATTLOG_COUNT_CACHE_SECONDS = 24 * 3600


def _text(body, status=200):
    return HttpResponse(body, status=status, content_type="text/plain")


def _device_timezone(device):
    if device.company_id:
        return device.company_id.get_timezone()
    return ZoneInfo(settings.TIME_ZONE)


def _ip_allowed(device, request):
    networks = device.allowed_source_networks()
    if not networks:
        return True
    try:
        client = ipaddress.ip_address(get_client_ip(request))
    except ValueError:
        return False
    return any(
        client.version == network.version and client in network
        for network in networks
    )


def _authorised_device(request):
    """
    Return (device, None) for an accepted device, or (None, response).
    Rejections are logged once per serial number per window, since a
    rejected device keeps retrying every few seconds.
    """
    serial_number = (request.GET.get("SN") or "").strip()
    if not serial_number:
        return None, _text("Missing SN", status=400)

    device = (
        BiometricDevices.objects.entire()
        .select_related("company_id")
        .filter(
            serial_number=serial_number,
            machine_type__in=BiometricDevices.PUSH_DEVICE_TYPES,
            is_active=True,
        )
        .first()
    )
    reason = None
    if device is None:
        reason = "unregistered or archived serial number"
    else:
        try:
            if not _ip_allowed(device, request):
                reason = "source address not allowed"
        except ValueError:
            reason = "invalid source address list on the device"

    if reason:
        if cache.add(
            f"biometric:adms:rejected:{serial_number}", 1, UNKNOWN_DEVICE_LOG_SECONDS
        ):
            logger.warning(
                "ADMS request from SN=%s rejected: %s (client %s)",
                serial_number,
                reason,
                get_client_ip(request),
            )
        return None, _text("Device not registered", status=403)

    now = timezone.now()
    if not device.last_push_at or now - device.last_push_at >= LAST_SEEN_INTERVAL:
        BiometricDevices.objects.entire().filter(pk=device.pk).update(
            last_push_at=now
        )
        device.last_push_at = now
    return device, None


def _utc_offset_hours(tz):
    offset = timezone.now().astimezone(tz).utcoffset() or timedelta()
    hours = offset.total_seconds() / 3600
    return int(hours) if hours.is_integer() else hours


def handshake_options(device):
    """Options the device applies after its handshake."""
    stamp = device.push_attlog_stamp or "0"
    lines = [
        f"GET OPTION FROM: {device.serial_number}",
        "Stamp=9999",
        "OpStamp=9999",
        f"ATTLOGStamp={stamp}",
        f"AttLogStamp={stamp}",
        "OPERLOGStamp=9999",
        "ATTPHOTOStamp=9999",
        "ErrorDelay=30",
        "Delay=10",
        "TransTimes=00:00;14:05",
        "TransInterval=1",
        "TransFlag=1",
        f"TimeZone={_utc_offset_hours(_device_timezone(device))}",
        "Realtime=1",
        "Encrypt=None",
    ]
    return "\r\n".join(lines) + "\r\n"


def parse_attlog(body):
    """
    Parse ATTLOG lines: PIN, "YYYY-MM-DD HH:MM:SS", status, verify, ...
    Returns (records, bad_line_count). Records are sorted by time so check-in
    and check-out are applied in the order they happened.
    """
    records = []
    bad = 0
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split("\t")]
        try:
            pin = parts[0]
            if not pin:
                raise ValueError("empty PIN")
            punched = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S")
        except (IndexError, ValueError):
            bad += 1
            logger.warning("ADMS: unreadable ATTLOG line %r", line[:200])
            continue
        records.append(
            {
                "pin": pin,
                "local_time": punched,
                "status": _int_or_none(parts, 2),
                "verify": _int_or_none(parts, 3),
            }
        )
    records.sort(key=lambda record: record["local_time"])
    return records, bad


def _int_or_none(parts, index):
    try:
        return int(parts[index])
    except (IndexError, ValueError):
        return None


def _find_employee(device, pin):
    """Return (employee, error message)."""
    employees = Employee.objects.entire().filter(badge_id=pin, is_active=True)
    if device.company_id_id:
        employees = employees.filter(employee_work_info__company_id=device.company_id_id)
    matches = list(employees.select_related("employee_user_id")[:2])
    if not matches:
        return None, "No active employee with this Badge ID in the device's company."
    if len(matches) > 1:
        return None, "More than one active employee has this Badge ID."
    return matches[0], ""


def _choose_action(device, status, employee):
    direction = device.device_direction
    if direction == "in":
        return "clock_in"
    if direction == "out":
        return "clock_out"
    if direction == "system":
        if status in IN_STATUS_CODES:
            return "clock_in"
        if status in OUT_STATUS_CODES:
            return "clock_out"
    # Alternate, or a status code that says nothing about direction.
    return "clock_out" if latest_open_activity(employee) else "clock_in"


def _apply_punch(device, record, punch_at, log):
    """Fill log.result, log.employee_id and log.message for one record."""
    registered_on = timezone.localtime(device.created_at, punch_at.tzinfo).date()
    if punch_at.date() < registered_on:
        log.result = "ignored"
        log.message = "Punch is older than the day the device was added."
        return

    employee, error = _find_employee(device, record["pin"])
    if employee is None:
        log.result = "unmatched"
        log.message = error
        return
    log.employee_id = employee
    if employee.employee_user_id is None:
        log.result = "failed"
        log.message = "Employee has no user account."
        return

    action = _choose_action(device, record["status"], employee)
    if action == "clock_out" and not latest_open_activity(employee):
        log.result = "ignored"
        log.message = "Check-out without an open check-in."
        return

    local = punch_at.astimezone(employee.get_timezone())
    punch = clock_in if action == "clock_in" else clock_out
    with transaction.atomic():
        punch(
            Request(
                user=employee.employee_user_id,
                date=local.date(),
                time=local.time(),
                datetime=local,
            )
        )
    log.result = action


def process_record(device, record, tz=None):
    """
    Store and apply one ATTLOG record. Returns the log, or None when the same
    punch was already received.
    """
    tz = tz or _device_timezone(device)
    punch_at = record["local_time"].replace(tzinfo=tz)
    try:
        with transaction.atomic():
            log = BiometricPushLog.objects.create(
                device_id=device,
                user_id=record["pin"],
                punch_time=punch_at,
                status_code=record["status"],
                verify_code=record["verify"],
                result="failed",
            )
    except IntegrityError:
        return None

    try:
        _apply_punch(device, record, punch_at, log)
    except Exception as error:
        logger.exception(
            "ADMS: punch for PIN=%s from SN=%s failed",
            record["pin"],
            device.serial_number,
        )
        log.result = "failed"
        log.message = str(error)[:255]
    log.save(update_fields=["result", "employee_id", "message"])
    return log


def _receive_attlog(device, body, stamp):
    records, bad = parse_attlog(body)
    tz = _device_timezone(device)
    results = {}
    for record in records:
        log = process_record(device, record, tz)
        key = log.result if log else "duplicate"
        results[key] = results.get(key, 0) + 1

    updates = {}
    if records:
        latest = records[-1]["local_time"]
        updates["last_fetch_date"] = latest.date()
        updates["last_fetch_time"] = latest.time()
    if stamp:
        updates["push_attlog_stamp"] = stamp[:50]
    if updates:
        BiometricDevices.objects.entire().filter(pk=device.pk).update(**updates)

    logger.info(
        "ADMS: SN=%s sent %s records (%s unreadable): %s",
        device.serial_number,
        len(records),
        bad,
        results,
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def cdata(request):
    """Handshake (GET) and record upload (POST)."""
    device, rejection = _authorised_device(request)
    if rejection:
        return rejection
    if request.method == "GET":
        return _text(handshake_options(device))

    table = (request.GET.get("table") or "").upper()
    if table == "ATTLOG":
        body = request.body.decode("utf-8", errors="replace")
        _receive_attlog(device, body, request.GET.get("Stamp"))
    else:
        logger.debug("ADMS: SN=%s sent table %s, ignored", device.serial_number, table)
    return _text("OK")


@csrf_exempt
@require_GET
def getrequest(request):
    """
    Command poll. INFO carries the device's attendance-log count; when it
    grows, ask the device to upload, in case realtime upload is off.
    """
    device, rejection = _authorised_device(request)
    if rejection:
        return rejection
    info = request.GET.get("INFO")
    if info:
        try:
            count = int(info.split(",")[3])
        except (IndexError, ValueError):
            count = None
        if count is not None:
            key = f"biometric:adms:attlog_count:{device.pk}"
            previous = cache.get(key)
            cache.set(key, count, ATTLOG_COUNT_CACHE_SECONDS)
            if previous is not None and count > previous:
                return _text("C:DATA UPDATE\r\n")
    return _text("OK")


@csrf_exempt
@require_POST
def devicecmd(request):
    """Result of a command sent through getrequest."""
    device, rejection = _authorised_device(request)
    if rejection:
        return rejection
    logger.debug(
        "ADMS: SN=%s command result %r",
        device.serial_number,
        request.body[:200],
    )
    return _text("OK")


@csrf_exempt
@require_GET
def ping(request):
    """Keep-alive some firmware sends while uploading."""
    device, rejection = _authorised_device(request)
    if rejection:
        return rejection
    return _text("OK")
