from django.db import migrations


def create_producer_critic_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    view_permissions = Permission.objects.filter(codename__startswith='view_')

    producer_group, _ = Group.objects.get_or_create(name='PRODUCER')
    producer_group.permissions.set(
        list(view_permissions) + list(
            Permission.objects.filter(codename__in=['change_review', 'change_pressarticle'])
        )
    )

    critic_group, _ = Group.objects.get_or_create(name='CRITIC')
    critic_group.permissions.set(
        list(view_permissions) + list(
            Permission.objects.filter(codename__in=['add_pressarticle', 'change_pressarticle', 'delete_pressarticle'])
        )
    )

    admin_group = Group.objects.filter(name='ADMIN').first()
    if admin_group:
        admin_group.permissions.set(Permission.objects.all())


def delete_producer_critic_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['PRODUCER', 'CRITIC']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_show_producer_usermeta_affiliate_tier_pressarticle'),
    ]

    operations = [
        migrations.RunPython(create_producer_critic_groups, delete_producer_critic_groups),
    ]
