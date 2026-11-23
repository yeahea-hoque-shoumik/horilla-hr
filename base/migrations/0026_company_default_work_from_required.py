import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    # Separate from the backfill: PostgreSQL cannot alter a table that has
    # pending FK trigger events from the same transaction.
    dependencies = [("base", "0025_company_default_work_from")]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="default_work_from",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="default_for_companies",
                to="base.workfrom",
                verbose_name="Default Work From",
                help_text="Used at check-in for employees without their own default.",
            ),
        ),
    ]
