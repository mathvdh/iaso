# Generated by Django 2.0 on 2018-12-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("vector_control", "0004_auto_20181211_1233")]

    operations = [
        migrations.AlterField(
            model_name="site",
            name="habitat",
            field=models.TextField(
                blank=True,
                choices=[
                    ("bush", "Buisson"),
                    ("fish_pond", "Etang à poissons"),
                    ("farm", "Ferme"),
                    ("forest", "Forêt"),
                    ("unknown", "Inconnu"),
                    ("lake", "Lac"),
                    ("river", "Rivière"),
                    ("road", "Route"),
                    ("stream", "Ruisseau"),
                ],
                max_length=255,
                null=True,
            ),
        )
    ]
