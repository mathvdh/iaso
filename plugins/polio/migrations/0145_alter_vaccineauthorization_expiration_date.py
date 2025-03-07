# Generated by Django 3.2.15 on 2023-09-13 09:13

import datetime

from django.db import migrations, models


# handle old records with a None date.
def populate_expiration_date(apps, schema_editor):
    VaccineAuthorization = apps.get_model("polio", "VaccineAuthorization")

    VaccineAuthorization.objects.filter(expiration_date=None).update(expiration_date=datetime.datetime.now())


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0144_alter_vaccineauthorization_status"),
    ]

    operations = [
        migrations.RunPython(populate_expiration_date, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="vaccineauthorization",
            name="expiration_date",
            field=models.DateField(),
        ),
    ]
