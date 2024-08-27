# Generated by Django 4.2.14 on 2024-08-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0195_migrate_chronogramtask_user_in_charge"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chronogramtask",
            name="user_in_charge",
        ),
        migrations.RenameField(
            model_name="chronogramtask",
            old_name="user_in_charge_new",
            new_name="user_in_charge",
        ),
    ]
