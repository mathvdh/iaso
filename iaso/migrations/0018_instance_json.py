# Generated by Django 2.2.4 on 2019-08-14 14:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("iaso", "0017_auto_20190809_1205")]

    operations = [
        migrations.AddField(
            model_name="instance",
            name="json",
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        )
    ]
