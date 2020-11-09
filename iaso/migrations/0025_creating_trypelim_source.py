# Generated by Django 2.2.4 on 2019-09-29 09:32

from django.db import migrations, models


def forwards_func():
    from iaso.models import DataSource, SourceVersion, OrgUnit

    ds = DataSource.objects.get_or_create(name="trypelim")
    ds = ds[0]
    version = SourceVersion.objects.get_or_create(data_source=ds, number=1)
    version = version[0]
    OrgUnit.objects.exclude(source="kemri").update(version=version)


def reverse_func():
    pass


class Migration(migrations.Migration):
    dependencies = [("iaso", "0024_altering_fields_on_sources")]

    class Migration(migrations.Migration):
        dependencies = []

        operations = [migrations.RunPython(forwards_func, reverse_func)]
