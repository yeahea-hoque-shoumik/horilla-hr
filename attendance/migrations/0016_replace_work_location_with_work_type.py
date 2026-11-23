"""Check-in now records a WorkType, so the separate WorkLocation list is removed."""

import django.db.models.deletion
from django.db import migrations, models


def copy_locations_to_work_types(apps, schema_editor):
    """Keep choices already recorded on databases that applied 0015."""
    WorkLocation = apps.get_model("attendance", "WorkLocation")
    WorkType = apps.get_model("base", "WorkType")
    Attendance = apps.get_model("attendance", "Attendance")
    AttendanceActivity = apps.get_model("attendance", "AttendanceActivity")

    for location in WorkLocation.objects.all():
        name = location.name[:50]
        work_type = WorkType.objects.filter(
            company_id=location.company_id_id, work_type=name
        ).first()
        if work_type is None:
            work_type = WorkType.objects.create(work_type=name)
            work_type.company_id.add(location.company_id_id)
        AttendanceActivity.objects.filter(work_location=location).update(
            work_type_id=work_type
        )
        Attendance.objects.filter(work_location=location).update(
            work_type_id=work_type
        )


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0021_company_timezone"),
        ("attendance", "0015_work_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendanceactivity",
            name="work_type_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="base.worktype",
                verbose_name="Work Type",
            ),
        ),
        migrations.AddField(
            model_name="historicalattendanceactivity",
            name="work_type_id",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="base.worktype",
                verbose_name="Work Type",
            ),
        ),
        migrations.RunPython(copy_locations_to_work_types, migrations.RunPython.noop),
        migrations.RemoveField(model_name="attendance", name="work_location"),
        migrations.RemoveField(model_name="attendanceactivity", name="work_location"),
        migrations.RemoveField(model_name="historicalattendance", name="work_location"),
        migrations.RemoveField(
            model_name="historicalattendanceactivity", name="work_location"
        ),
        migrations.DeleteModel(name="WorkLocation"),
    ]
