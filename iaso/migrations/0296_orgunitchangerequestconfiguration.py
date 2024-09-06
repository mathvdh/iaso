# Generated by Django 4.2.13 on 2024-08-29 10:04

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("iaso", "0295_merge_20240819_1249"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrgUnitChangeRequestConfiguration",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted_at", models.DateTimeField(blank=True, default=None, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("org_units_editable", models.BooleanField(default=True)),
                (
                    "editable_fields",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=30),
                        blank=True,
                        default=list,
                        help_text="List of fields that can edited in an OrgUnit",
                        size=None,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="org_unit_change_request_configurations_created_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "editable_reference_forms",
                    models.ManyToManyField(
                        blank=True, related_name="org_unit_change_request_configurations", to="iaso.form"
                    ),
                ),
                (
                    "org_unit_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="iaso.orgunittype"),
                ),
                (
                    "other_groups",
                    models.ManyToManyField(
                        blank=True, related_name="org_unit_change_request_configurations", to="iaso.group"
                    ),
                ),
                (
                    "group_sets",
                    models.ManyToManyField(
                        blank=True, related_name="org_unit_change_request_configurations", to="iaso.groupset"
                    ),
                ),
                (
                    "possible_parent_types",
                    models.ManyToManyField(
                        blank=True,
                        related_name="org_unit_change_request_configurations_parent_level",
                        to="iaso.orgunittype",
                    ),
                ),
                (
                    "possible_types",
                    models.ManyToManyField(
                        blank=True,
                        related_name="org_unit_change_request_configurations_same_level",
                        to="iaso.orgunittype",
                    ),
                ),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="iaso.project")),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="org_unit_change_request_configurations_updated_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Org unit change request configuration",
                "indexes": [
                    models.Index(fields=["project"], name="iaso_orguni_project_6d2cbe_idx"),
                    models.Index(fields=["org_unit_type"], name="iaso_orguni_org_uni_a6fdd1_idx"),
                ],
                "unique_together": {("project", "org_unit_type")},
            },
        ),
    ]
