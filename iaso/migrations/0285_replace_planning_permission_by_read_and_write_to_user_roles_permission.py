# Generated by Django 4.2.13 on 2024-06-10 08:28

from django.db import migrations


def link_iaso_planning_write_and_read_to_user_roles(apps, schema_editor):
    permission = apps.get_model("auth", "Permission")
    userRole = apps.get_model("iaso", "UserRole")
    old_planning_permission = permission.objects.filter(codename="iaso_planning").first()
    user_roles_linked_old_permission = userRole.objects.filter(group__permissions=old_planning_permission)
    new_planning_permissions = permission.objects.filter(codename__in=["iaso_planning_write", "iaso_planning_read"])

    for user_role in user_roles_linked_old_permission:
        user_role.group.permissions.remove(old_planning_permission)
        user_role.group.permissions.add(*new_planning_permissions)


def unlink_iaso_planning_write_and_read_to_user_roles(apps, schema_editor):
    permission = apps.get_model("auth", "Permission")
    userRole = apps.get_model("iaso", "UserRole")
    old_planning_permissions = permission.objects.filter(codename__in=["iaso_planning_write", "iaso_planning_read"])
    users_linked_old_permissions = userRole.objects.filter(group__permissions__in=old_planning_permissions)
    new_planning_permission = permission.objects.filter(codename="iaso_planning").first()

    for user_role in users_linked_old_permissions:
        user_role.group.permissions.remove(*old_planning_permissions)
        user_role.group.permissions.add(new_planning_permission)


class Migration(migrations.Migration):
    dependencies = [
        (
            "iaso",
            "0284_replace_registry_permission_by_read_and_write_to_user_roles_permission",
        ),
    ]

    operations = [
        migrations.RunPython(
            link_iaso_planning_write_and_read_to_user_roles, unlink_iaso_planning_write_and_read_to_user_roles
        )
    ]
