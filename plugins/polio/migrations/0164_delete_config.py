# Generated by Django 4.2.9 on 2024-01-25 11:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0163_move_config_model_data_to_iaso"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Config",
        ),
    ]
