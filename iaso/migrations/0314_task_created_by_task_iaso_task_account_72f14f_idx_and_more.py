# Generated by Django 4.2.16 on 2024-12-17 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("iaso", "0313_page_superset_dashboard_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunSQL(
            sql="UPDATE iaso_task SET created_by_id = launcher_id;",
            reverse_sql="",
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["account"], name="iaso_task_account_72f14f_idx"),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["created_at"], name="iaso_task_created_25fae0_idx"),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["created_by"], name="iaso_task_created_573360_idx"),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["name"], name="iaso_task_name_5f0019_idx"),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["status"], name="iaso_task_status_bb234e_idx"),
        ),
    ]
