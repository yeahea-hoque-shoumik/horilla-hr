from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0016_replace_work_location_with_work_type'),
        ('base', '0022_rename_work_type_to_work_from'),
    ]

    operations = [
        migrations.RenameField(model_name='attendance', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='attendanceactivity', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='historicalattendance', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='historicalattendanceactivity', old_name='work_type_id', new_name='work_from_id'),
    ]
