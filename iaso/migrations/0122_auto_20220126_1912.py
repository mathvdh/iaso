# Generated by Django 3.1.14 on 2022-01-26 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("iaso", "0121_entity_account"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="account",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="iaso.account"),
        ),
    ]
