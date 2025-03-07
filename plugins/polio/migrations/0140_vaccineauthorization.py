# Generated by Django 3.2.15 on 2023-08-09 06:48

import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0226_merge_20230724_1245"),
        ("polio", "0139_merge_20230724_1542"),
    ]

    operations = [
        migrations.CreateModel(
            name="VaccineAuthorization",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted_at", models.DateTimeField(blank=True, default=None, null=True)),
                ("expiration_date", models.DateField(auto_now_add=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.IntegerField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ongoing", "Ongoing"),
                            ("signature", "Sent for signature"),
                            ("validated", "Validated"),
                            ("expired", "Expired"),
                        ],
                        max_length=200,
                    ),
                ),
                ("comment", models.TextField(blank=True, max_length=250, null=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="vaccineauthorization",
                        to="iaso.account",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vaccineauthorization",
                        to="iaso.orgunit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
