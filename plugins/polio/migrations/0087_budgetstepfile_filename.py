# Generated by Django 3.2.15 on 2022-10-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polio", "0086_rename_budgetstepfiles_budgetstepfile"),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetstepfile",
            name="filename",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
