"""
Carry the WorkType to WorkFrom rename into stored values and database names.

Permission rows are updated in place so user and group grants keep working.
Constraint, index and sequence names are renamed on PostgreSQL because Django
leaves them unchanged when a model or field is renamed.
"""

import re

from django.db import migrations

FORWARD = (
    ("Work Types", "Work From Options"),
    ("Work types", "Work from options"),
    ("work types", "work from options"),
    ("Work Type", "Work From"),
    ("Work type", "Work from"),
    ("work type", "work from"),
    ("WorkType", "WorkFrom"),
    ("Worktype", "WorkFrom"),
    ("workType", "workFrom"),
    ("worktype", "workfrom"),
    ("work_type", "work_from"),
    ("work-type", "work-from"),
)
BACKWARD = (
    ("Work From Options", "Work Types"),
    ("Work from options", "Work types"),
    ("work from options", "work types"),
    ("Work From", "Work Type"),
    ("Work from", "Work type"),
    ("work from", "work type"),
    ("WorkFrom", "WorkType"),
    ("workFrom", "workType"),
    ("workfrom", "worktype"),
    ("work_from", "work_type"),
    ("work-from", "work-type"),
)
STORED_TEXT = (
    ("auth", "Permission", ("codename", "name")),
    ("horilla_tour", "Tour", ("title", "slug", "description", "page_match")),
    ("horilla_tour", "TourStep", ("title", "description", "element_selector")),
    ("horilla_views", "ActiveTab", ("path", "tab_target")),
)


def _translator(pairs, backward):
    mapping = dict(pairs)
    # "work from home" is ordinary text that existed before this rename.
    guard = r"(?![ -]home)" if backward else ""
    pattern = re.compile(
        r"(?<![Nn]et)(?<![Ff]rame)(?<![Hh]ome)(%s)%s"
        % ("|".join(re.escape(key) for key, _ in pairs), guard)
    )
    return lambda value: pattern.sub(lambda match: mapping[match.group(1)], value)


def _update_rows(apps, pairs, backward):
    translate = _translator(pairs, backward)
    for app_label, model_name, fields in STORED_TEXT:
        model = apps.get_model(app_label, model_name)
        for row in model.objects.all().only("pk", *fields).iterator():
            changes = {
                field: translate(getattr(row, field))
                for field in fields
                if getattr(row, field)
                and translate(getattr(row, field)) != getattr(row, field)
            }
            if changes:
                model.objects.filter(pk=row.pk).update(**changes)


def _rename_database_objects(schema_editor, old_tokens, new_tokens):
    if schema_editor.connection.vendor != "postgresql":
        return

    def renamed(name):
        for old, new in zip(old_tokens, new_tokens):
            name = name.replace(old, new)
        return name

    quote = schema_editor.quote_name
    pattern = "|".join(old_tokens)
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT con.conname, rel.relname
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            JOIN pg_namespace ns ON ns.oid = rel.relnamespace
            WHERE ns.nspname = current_schema() AND con.conname ~ %s
            """,
            [pattern],
        )
        for name, table in cursor.fetchall():
            cursor.execute(
                f"ALTER TABLE {quote(table)} "
                f"RENAME CONSTRAINT {quote(name)} TO {quote(renamed(name))}"
            )
        cursor.execute(
            """
            SELECT indexname FROM pg_indexes
            WHERE schemaname = current_schema() AND indexname ~ %s
            """,
            [pattern],
        )
        for (name,) in cursor.fetchall():
            cursor.execute(f"ALTER INDEX {quote(name)} RENAME TO {quote(renamed(name))}")
        cursor.execute(
            """
            SELECT sequencename FROM pg_sequences
            WHERE schemaname = current_schema() AND sequencename ~ %s
            """,
            [pattern],
        )
        for (name,) in cursor.fetchall():
            cursor.execute(
                f"ALTER SEQUENCE {quote(name)} RENAME TO {quote(renamed(name))}"
            )


def forwards(apps, schema_editor):
    _update_rows(apps, FORWARD, backward=False)
    apps.get_model("payroll", "Allowance").objects.filter(
        based_on="work_type_id"
    ).update(based_on="work_from_id")
    _rename_database_objects(
        schema_editor, ("worktype", "work_type"), ("workfrom", "work_from")
    )


def backwards(apps, schema_editor):
    _rename_database_objects(
        schema_editor, ("workfrom", "work_from"), ("worktype", "work_type")
    )
    apps.get_model("payroll", "Allowance").objects.filter(
        based_on="work_from_id"
    ).update(based_on="work_type_id")
    _update_rows(apps, BACKWARD, backward=True)


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "__latest__"),
        ("contenttypes", "__latest__"),
        ("base", "0023_work_from_labels"),
        ("attendance", "0018_work_from_labels"),
        ("employee", "0012_work_from_labels"),
        ("payroll", "0014_work_from_labels"),
        ("horilla_tour", "0088_alter_tour_is_active_alter_tourprogress_is_active_and_more"),
        ("horilla_views", "0003_alter_activegroup_is_active_and_more"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
