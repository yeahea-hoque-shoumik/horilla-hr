"""ADMS push receiver for ZKTeco SenseFace 2A style devices."""

from datetime import datetime, time, timezone as dt_timezone

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings

from attendance.models import AttendanceActivity
from base.models import EmployeeShift, EmployeeShiftDay, EmployeeShiftSchedule
from biometric.adms import parse_attlog
from biometric.models import BiometricDevices, BiometricPushLog
from biometric.views import test_push_device_connection
from horilla.horilla_middlewares import set_selected_company
from horilla.testkit import make_company, make_employee

SN = "SF2A0001"


def line(pin, stamp, status=0, verify=15):
    return f"{pin}\t{stamp}\t{status}\t{verify}\t0\t0\t0"


@override_settings(TIME_ZONE="Asia/Dhaka")
class ADMSBase(TestCase):
    def setUp(self):
        cache.clear()
        set_selected_company(None)
        for name in ("monday", "tuesday", "wednesday", "thursday", "friday"):
            EmployeeShiftDay.objects.get_or_create(day=name)
        self.company = make_company("Push Co", timezone="Asia/Dhaka")
        self.other_company = make_company("Other Co", timezone="Asia/Dhaka")
        shift = EmployeeShift.objects.create(employee_shift="Day")
        EmployeeShiftSchedule.objects.create(
            day=EmployeeShiftDay.objects.get(day="wednesday"),
            shift_id=shift,
            minimum_working_hour="08:00",
            start_time=time(9),
            end_time=time(17),
        )
        self.employee = make_employee(
            company=self.company, email="push@test.horilla", shift=shift
        )
        self.employee.badge_id = "1001"
        self.employee.save()
        self.device = BiometricDevices.objects.create(
            name="Lobby SenseFace",
            machine_type="zkpush",
            serial_number=SN,
            company_id=self.company,
        )
        # Added well before the punches the tests send.
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            created_at=datetime(2026, 1, 1, tzinfo=dt_timezone.utc)
        )
        self.device.refresh_from_db()
        self.client = Client(enforce_csrf_checks=True)

    def tearDown(self):
        set_selected_company(None)

    def push(self, *lines, sn=SN, stamp="100", **extra):
        return self.client.post(
            f"/iclock/cdata?SN={sn}&table=ATTLOG&Stamp={stamp}",
            data="\n".join(lines),
            content_type="text/plain",
            **extra,
        )

    def activities(self):
        return AttendanceActivity.objects.filter(employee_id=self.employee)


class HandshakeTests(ADMSBase):
    def test_registered_device_gets_options(self):
        response = self.client.get(f"/iclock/cdata?SN={SN}&options=all")
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn(f"GET OPTION FROM: {SN}", body)
        self.assertIn("TimeZone=6", body)
        self.assertIn("ATTLOGStamp=0", body)
        self.device.refresh_from_db()
        self.assertIsNotNone(self.device.last_push_at)

    def test_saved_stamp_is_returned(self):
        self.push(line("1001", "2026-11-18 09:05:00"), stamp="12345")
        body = self.client.get(f"/iclock/cdata?SN={SN}").content.decode()
        self.assertIn("ATTLOGStamp=12345", body)

    def test_unknown_serial_is_rejected(self):
        self.assertEqual(self.client.get("/iclock/cdata?SN=NOPE").status_code, 403)
        self.assertEqual(self.client.get("/iclock/cdata").status_code, 400)

    def test_archived_device_is_rejected(self):
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            is_active=False
        )
        self.assertEqual(self.client.get(f"/iclock/cdata?SN={SN}").status_code, 403)
        self.assertEqual(
            self.push(line("1001", "2026-11-18 09:05:00")).status_code, 403
        )
        self.assertFalse(self.activities().exists())

    def test_pull_device_serial_is_not_accepted(self):
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            machine_type="zk"
        )
        self.assertEqual(self.client.get(f"/iclock/cdata?SN={SN}").status_code, 403)

    def test_source_address_allowlist(self):
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            machine_ip="203.0.113.0/24"
        )
        url = f"/iclock/cdata?SN={SN}"
        self.assertEqual(
            self.client.get(url, REMOTE_ADDR="198.51.100.5").status_code, 403
        )
        self.assertEqual(
            self.client.get(url, REMOTE_ADDR="203.0.113.7").status_code, 200
        )


class AttlogTests(ADMSBase):
    def test_check_in_and_out_by_badge_id(self):
        response = self.push(
            line("1001", "2026-11-18 17:10:00", status=1),
            line("1001", "2026-11-18 09:05:00", status=0),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")
        activity = self.activities().get()
        self.assertEqual(str(activity.attendance_date), "2026-11-18")
        self.assertIsNotNone(activity.clock_out)
        results = list(
            BiometricPushLog.objects.order_by("punch_time").values_list(
                "result", flat=True
            )
        )
        self.assertEqual(results, ["clock_in", "clock_out"])
        self.device.refresh_from_db()
        self.assertEqual(self.device.push_attlog_stamp, "100")
        self.assertEqual(str(self.device.last_fetch_time), "17:10:00")

    def test_device_time_is_read_in_company_zone(self):
        self.push(line("1001", "2026-11-18 09:05:00"))
        log = BiometricPushLog.objects.get()
        self.assertEqual(
            log.punch_time, datetime(2026, 11, 18, 3, 5, tzinfo=dt_timezone.utc)
        )

    def test_repeated_push_applies_once(self):
        records = [
            line("1001", "2026-11-18 09:05:00", status=0),
            line("1001", "2026-11-18 17:10:00", status=1),
        ]
        self.push(*records)
        self.push(*records)
        self.assertEqual(self.activities().count(), 1)
        self.assertEqual(BiometricPushLog.objects.count(), 2)

    def test_unknown_pin_is_logged_not_punched(self):
        self.push(line("9999", "2026-11-18 09:05:00"))
        log = BiometricPushLog.objects.get()
        self.assertEqual(log.result, "unmatched")
        self.assertIsNone(log.employee_id)
        self.assertFalse(AttendanceActivity.objects.exists())

    def test_badge_in_other_company_is_not_matched(self):
        outsider = make_employee(
            company=self.other_company, email="outsider@test.horilla"
        )
        outsider.badge_id = "2002"
        outsider.save()
        self.push(line("2002", "2026-11-18 09:05:00"))
        self.assertEqual(BiometricPushLog.objects.get().result, "unmatched")
        self.assertFalse(
            AttendanceActivity.objects.filter(employee_id=outsider).exists()
        )

    def test_unknown_status_alternates(self):
        self.push(
            line("1001", "2026-11-18 09:05:00", status=255),
            line("1001", "2026-11-18 17:10:00", status=255),
        )
        activity = self.activities().get()
        self.assertIsNotNone(activity.clock_out)

    def test_in_device_ignores_status(self):
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            device_direction="in"
        )
        self.push(line("1001", "2026-11-18 09:05:00", status=1))
        self.assertEqual(BiometricPushLog.objects.get().result, "clock_in")
        self.assertIsNone(self.activities().get().clock_out)

    def test_check_out_without_check_in_is_ignored(self):
        self.push(line("1001", "2026-11-18 17:10:00", status=1))
        self.assertEqual(BiometricPushLog.objects.get().result, "ignored")
        self.assertFalse(self.activities().exists())

    def test_backlog_before_device_was_added_is_ignored(self):
        self.push(line("1001", "2025-12-30 09:05:00"))
        self.assertEqual(BiometricPushLog.objects.get().result, "ignored")
        self.assertFalse(self.activities().exists())

    def test_other_tables_are_acknowledged(self):
        response = self.client.post(
            f"/iclock/cdata?SN={SN}&table=OPERLOG",
            data="OPLOG 4\t0\t2026-11-18 09:00:00",
            content_type="text/plain",
        )
        self.assertEqual(response.content, b"OK")
        self.assertFalse(BiometricPushLog.objects.exists())

    def test_unreadable_lines_are_skipped(self):
        records, bad = parse_attlog("garbage\n1001\tnot-a-date\n\n")
        self.assertEqual((records, bad), ([], 2))


class PollTests(ADMSBase):
    def test_new_log_count_requests_upload(self):
        url = f"/iclock/getrequest?SN={SN}&INFO=Ver 8.0,2,0,10,192.168.0.20"
        self.assertEqual(self.client.get(url).content, b"OK")
        url = f"/iclock/getrequest?SN={SN}&INFO=Ver 8.0,2,0,11,192.168.0.20"
        self.assertEqual(self.client.get(url).content, b"C:DATA UPDATE\r\n")

    def test_devicecmd_and_ping(self):
        response = self.client.post(
            f"/iclock/devicecmd?SN={SN}", data="ID=1&Return=0", content_type="text/plain"
        )
        self.assertEqual(response.content, b"OK")
        self.assertEqual(self.client.get(f"/iclock/ping?SN={SN}").content, b"OK")

    def test_aspx_paths(self):
        self.assertEqual(self.client.get(f"/iclock/cdata.aspx?SN={SN}").status_code, 200)


class DeviceSetupTests(ADMSBase):
    def test_serial_number_required(self):
        device = BiometricDevices(name="No SN", machine_type="zkpush")
        with self.assertRaises(ValidationError) as caught:
            device.clean()
        self.assertIn("serial_number", caught.exception.message_dict)

    def test_bad_source_list_rejected(self):
        device = BiometricDevices(
            name="Bad IP", machine_type="zkpush", serial_number="X1", machine_ip="lobby"
        )
        with self.assertRaises(ValidationError) as caught:
            device.clean()
        self.assertIn("machine_ip", caught.exception.message_dict)

    def test_connection_status_follows_last_contact(self):
        self.assertIn("No contact yet", test_push_device_connection(self.device))
        self.client.get(f"/iclock/cdata?SN={SN}")
        self.device.refresh_from_db()
        self.assertIn("Connection Successful", test_push_device_connection(self.device))


class DevicePageTests(ADMSBase):
    def setUp(self):
        super().setUp()
        from base.models import BiometricAttendance

        BiometricAttendance.objects.update_or_create(
            company_id=None, defaults={"is_installed": True}
        )
        admin = self.employee.employee_user_id
        admin.is_superuser = True
        admin.is_new_employee = False
        admin.save()
        self.page = Client()
        self.page.force_login(admin)

    def test_form_offers_push_type_and_serial_number(self):
        response = self.page.get("/biometric/biometric-device-add/", HTTP_HX_REQUEST="true")
        self.assertContains(response, 'value="zkpush"')
        self.assertContains(response, 'name="serial_number"')

    def test_card_shows_serial_and_hides_schedule(self):
        response = self.page.get("/biometric/biometric-card-view/", HTTP_HX_REQUEST="true")
        self.assertContains(response, SN)
        self.assertContains(response, "Last Contact")
        self.assertNotContains(response, f"biometric-device-schedule/{self.device.pk}/")

    def test_pull_device_card_still_offers_schedule(self):
        BiometricDevices.objects.entire().filter(pk=self.device.pk).update(
            machine_type="zk", machine_ip="192.168.0.20", port=4370
        )
        response = self.page.get("/biometric/biometric-card-view/", HTTP_HX_REQUEST="true")
        self.assertContains(response, f"biometric-device-schedule/{self.device.pk}/")
