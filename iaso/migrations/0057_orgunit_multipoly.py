# Generated by Django 2.1.11 on 2020-06-16 12:23

from django.db import migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [("iaso", "0056_merge_20200616_1223")]

    operations = [
        migrations.AlterField(
            model_name="orgunit",
            name="geom",
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="simplified_geom",
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name="orgunit",
            name="catchment",
            field=django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326),
        ),
        migrations.RunSQL(sql="update iaso_orgunit set geom=st_multi(geom) where geom is not null", reverse_sql=""),
        migrations.RunSQL(
            sql="update iaso_orgunit set simplified_geom=st_multi(simplified_geom) where simplified_geom is not null",
            reverse_sql="",
        ),
        migrations.RunSQL(
            sql="update iaso_orgunit set catchment=st_multi(catchment) where catchment is not null", reverse_sql=""
        ),
    ]
