# Generated by Django 3.2.22 on 2023-11-15 15:45

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("iaso", "0243_alter_instance_planning"),
        ("polio", "0151_alter_rounddatehistoryentry_reason"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationImport",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="uploads/polio_notifications/%Y-%m-%d-%H-%M/")),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("pending", "Pending"), ("done", "Done")], default="new", max_length=10
                    ),
                ),
                (
                    "errors",
                    models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="iaso.account")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="polio_notification_import_created_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Notification import",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("epid_number", models.CharField(max_length=50, unique=True)),
                (
                    "vdpv_category",
                    models.CharField(
                        choices=[
                            ("avdpv", "aVDPV"),
                            ("cvdpv1", "cVDPV1"),
                            ("cvdpv2", "cVDPV2"),
                            ("nopv2", "nOPV2"),
                            ("sabin", "Sabin"),
                            ("sabin1", "SABIN 1"),
                            ("sabin2", "SABIN 2"),
                            ("sabin3", "SABIN 3"),
                            ("vdpv", "VDPV"),
                            ("vdpv1", "VDPV1"),
                            ("vdpv2", "VDPV2"),
                            ("vdpv3", "VDPV3"),
                            ("vpv2", "VPV2"),
                            ("wpv1", "WPV1"),
                        ],
                        default="avdpv",
                        max_length=20,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("afp", "Accute Flaccid Paralysis"),
                            ("community", "Community"),
                            ("contact", "Contact"),
                            ("env", "Environmental"),
                            ("hc", "HC"),
                            ("other", "Other"),
                        ],
                        default="afp",
                        max_length=50,
                    ),
                ),
                ("vdpv_nucleotide_diff_sabin2", models.CharField(max_length=10)),
                ("lineage", models.CharField(blank=True, max_length=150)),
                ("closest_match_vdpv2", models.CharField(blank=True, max_length=150)),
                ("date_of_onset", models.DateField(blank=True, null=True)),
                ("date_results_received", models.DateField(blank=True, null=True)),
                ("site_name", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
                (
                    "import_raw_data",
                    models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
                ),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="iaso.account")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="polio_notification_created_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "import_source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="polio.notificationimport",
                    ),
                ),
                (
                    "org_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="polio_notifications",
                        to="iaso.orgunit",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="polio_notification_updated_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Notification",
            },
        ),
    ]
