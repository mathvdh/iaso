# Generated by Django 2.1.11 on 2019-11-27 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("iaso", "0018_profile")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="iaso_profile", to=settings.AUTH_USER_MODEL
            ),
        )
    ]
