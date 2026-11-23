from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0012_alter_allowance_is_active_and_more'),
        ('base', '0022_rename_work_type_to_work_from'),
    ]

    operations = [
        migrations.RenameField(model_name='allowance', old_name='work_type_per_attendance_amount', new_name='work_from_per_attendance_amount'),
        migrations.RenameField(model_name='allowance', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='contract', old_name='work_type', new_name='work_from'),
        migrations.RenameField(model_name='historicalcontract', old_name='work_type', new_name='work_from'),
    ]
