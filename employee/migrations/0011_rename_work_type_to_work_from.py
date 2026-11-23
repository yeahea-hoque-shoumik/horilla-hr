from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_work_info_timezone'),
        ('base', '0022_rename_work_type_to_work_from'),
    ]

    operations = [
        migrations.RenameField(model_name='employeeworkinformation', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='historicalemployeeworkinformation', old_name='work_type_id', new_name='work_from_id'),
    ]
