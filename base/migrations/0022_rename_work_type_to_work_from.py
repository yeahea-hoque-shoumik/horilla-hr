from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_company_timezone'),
        ('attendance', '0016_replace_work_location_with_work_type'),
        ('employee', '0010_work_info_timezone'),
        ('payroll', '0012_alter_allowance_is_active_and_more'),
    ]

    operations = [
        migrations.RenameModel(old_name='HistoricalRotatingWorkTypeAssign', new_name='HistoricalRotatingWorkFromAssign'),
        migrations.RenameModel(old_name='HistoricalWorkTypeRequest', new_name='HistoricalWorkFromRequest'),
        migrations.RenameModel(old_name='RotatingWorkType', new_name='RotatingWorkFrom'),
        migrations.RenameModel(old_name='RotatingWorkTypeAssign', new_name='RotatingWorkFromAssign'),
        migrations.RenameModel(old_name='WorkType', new_name='WorkFrom'),
        migrations.RenameModel(old_name='WorkTypeRequest', new_name='WorkFromRequest'),
        migrations.RenameModel(old_name='WorkTypeRequestComment', new_name='WorkFromRequestComment'),
        migrations.RenameField(model_name='historicalrotatingworkfromassign', old_name='rotating_work_type_id', new_name='rotating_work_from_id'),
        migrations.RenameField(model_name='historicalrotatingworkfromassign', old_name='current_work_type', new_name='current_work_from'),
        migrations.RenameField(model_name='historicalrotatingworkfromassign', old_name='next_work_type', new_name='next_work_from'),
        migrations.RenameField(model_name='historicalworkfromrequest', old_name='is_permanent_work_type', new_name='is_permanent_work_from'),
        migrations.RenameField(model_name='historicalworkfromrequest', old_name='work_type_changed', new_name='work_from_changed'),
        migrations.RenameField(model_name='historicalworkfromrequest', old_name='previous_work_type_id', new_name='previous_work_from_id'),
        migrations.RenameField(model_name='historicalworkfromrequest', old_name='work_type_id', new_name='work_from_id'),
        migrations.RenameField(model_name='rotatingworkfrom', old_name='work_type1', new_name='work_from1'),
        migrations.RenameField(model_name='rotatingworkfrom', old_name='work_type2', new_name='work_from2'),
        migrations.RenameField(model_name='rotatingworkfromassign', old_name='rotating_work_type_id', new_name='rotating_work_from_id'),
        migrations.RenameField(model_name='rotatingworkfromassign', old_name='current_work_type', new_name='current_work_from'),
        migrations.RenameField(model_name='rotatingworkfromassign', old_name='next_work_type', new_name='next_work_from'),
        migrations.RenameField(model_name='workfrom', old_name='work_type', new_name='work_from'),
        migrations.RenameField(model_name='workfromrequest', old_name='is_permanent_work_type', new_name='is_permanent_work_from'),
        migrations.RenameField(model_name='workfromrequest', old_name='work_type_changed', new_name='work_from_changed'),
        migrations.RenameField(model_name='workfromrequest', old_name='previous_work_type_id', new_name='previous_work_from_id'),
        migrations.RenameField(model_name='workfromrequest', old_name='work_type_id', new_name='work_from_id'),
    ]
