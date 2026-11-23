import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q


def backfill(apps, schema_editor):
    Company = apps.get_model("base", "Company")
    WorkFrom = apps.get_model("base", "WorkFrom")
    for company in Company.objects.filter(default_work_from__isnull=True):
        own = WorkFrom.objects.filter(company_id=company, is_active=True)
        shared = WorkFrom.objects.filter(company_id__isnull=True, is_active=True)
        options = WorkFrom.objects.filter(
            Q(company_id=company) | Q(company_id__isnull=True), is_active=True
        ).distinct()
        choice = (
            own.filter(work_from__icontains="office").order_by("id").first()
            or shared.filter(work_from__icontains="office").order_by("id").first()
            or options.order_by("id").first()
        )
        if choice is None:
            choice = WorkFrom.objects.create(work_from="Office")
            choice.company_id.add(company)
        company.default_work_from = choice
        company.save(update_fields=["default_work_from"])


class Migration(migrations.Migration):
    dependencies = [("base", "0024_work_from_stored_names")]

    operations = [
        migrations.AddField(
            model_name="company",
            name="default_work_from",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="default_for_companies",
                to="base.workfrom",
                verbose_name="Default Work From",
                help_text="Used at check-in for employees without their own default.",
            ),
        ),
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
