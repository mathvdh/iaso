# Generated by Django 3.1.12 on 2021-07-15 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0017_campaign_gpei_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="vials_requested",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
