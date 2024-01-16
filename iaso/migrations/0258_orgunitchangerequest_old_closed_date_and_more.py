# Generated by Django 4.2.9 on 2024-01-16 13:03

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0257_remove_orgunitchangerequest_reviewed_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_closed_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_groups",
            field=models.ManyToManyField(blank=True, related_name="+", to="iaso.group"),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, dim=3, geography=True, null=True, srid=4326
            ),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_opening_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_org_unit_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="iaso.orgunittype",
            ),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="iaso.orgunit",
            ),
        ),
        migrations.AddField(
            model_name="orgunitchangerequest",
            name="old_reference_instances",
            field=models.ManyToManyField(blank=True, related_name="+", to="iaso.instance"),
        ),
        migrations.AlterField(
            model_name="orgunitchangerequest",
            name="new_opening_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
