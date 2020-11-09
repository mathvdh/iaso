# Generated by Django 2.0 on 2019-05-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("vector_control", "0024_remove_trap_is_reference")]

    operations = [
        migrations.AlterField(
            model_name="catch",
            name="problem",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ants", "Fourmis"),
                    ("damaged", "Endommagé"),
                    ("fallen", "Tombé"),
                    ("forest", "Forêt"),
                    ("flood", "Innondé"),
                    ("missing", "Manquant"),
                    ("moved", "Bougé"),
                ],
                max_length=255,
                null=True,
            ),
        )
    ]
