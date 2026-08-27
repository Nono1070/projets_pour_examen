from django.db import migrations


def resync_admin_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    admin_group = Group.objects.filter(name='ADMIN').first()
    if admin_group:
        admin_group.permissions.set(Permission.objects.all())


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0015_show_published_rolerequest'),
    ]

    operations = [
        migrations.RunPython(resync_admin_permissions, noop),
    ]
