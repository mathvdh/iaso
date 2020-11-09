# Generated by Django 2.0 on 2019-06-17 12:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("iaso", "0001_initial")]

    operations = [
        migrations.AddField(model_name="orgunit", name="gps_source", field=models.TextField(blank=True, null=True)),
        migrations.AddField(
            model_name="orgunit",
            name="latitude",
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="orgunit",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name="orgunit",
            name="longitude",
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name="orgunit",
            name="org_level",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="iaso.OrgLevel"
            ),
        ),
        migrations.RemoveField(model_name="orglevel", name="org_unit_type"),
        migrations.AddField(
            model_name="orglevel", name="org_unit_type", field=models.ManyToManyField(blank=True, to="iaso.OrgUnitType")
        ),
        migrations.AlterField(
            model_name="orglevel",
            name="parent",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="iaso.OrgLevel"
            ),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="geom",
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(model_name="orgunit", name="geom_ref", field=models.IntegerField(blank=True, null=True)),
        migrations.AlterField(
            model_name="orgunit",
            name="geom_source",
            field=models.TextField(
                blank=True,
                choices=[
                    ("snis", "SNIS"),
                    ("ucla", "UCLA"),
                    ("pnltha", "PNL THA"),
                    ("derivated", "Derivated from actual data"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="org_unit_type",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="iaso.OrgUnitType"
            ),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="parent",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="iaso.OrgUnit"
            ),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="simplified_geom",
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="source",
            field=models.TextField(
                blank=True,
                choices=[
                    ("snis", "SNIS"),
                    ("ucla", "UCLA"),
                    ("pnltha", "PNL THA"),
                    ("derivated", "Derivated from actual data"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(model_name="orgunit", name="source_ref", field=models.TextField(blank=True, null=True)),
    ]
