from django.db import migrations


def resync_all_group_permissions(apps, schema_editor):
    """
    Meme piege que la migration 0010, reproduit dans la 0014 : les
    permissions d'un modele ne sont creees (signal post_migrate) qu'a la
    fin de la commande `migrate`, pas apres chaque migration individuelle.
    La 0014 assignait add/change/delete_pressarticle a CRITIC et
    change_pressarticle a PRODUCER dans le MEME `migrate` que la 0013 qui
    cree le modele PressArticle - ces permissions n'existaient pas encore
    au moment ou la 0014 s'est executee, donc PRODUCER et CRITIC ne les
    ont jamais recues. Meme constat pour MEMBER, jamais resynchronise
    depuis l'ajout de Reservation/PressArticle/RoleRequest.

    Cette migration tourne dans son propre `migrate`, donc apres que
    toutes les permissions existent deja - resynchronise les quatre
    groupes avec l'ensemble de permissions qu'ils sont censes avoir.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    view_permissions = Permission.objects.filter(codename__startswith='view_')

    admin_group = Group.objects.filter(name='ADMIN').first()
    if admin_group:
        admin_group.permissions.set(Permission.objects.all())

    member_group = Group.objects.filter(name='MEMBER').first()
    if member_group:
        member_group.permissions.set(view_permissions)

    producer_group = Group.objects.filter(name='PRODUCER').first()
    if producer_group:
        producer_group.permissions.set(
            list(view_permissions) + list(
                Permission.objects.filter(codename__in=['change_review', 'change_pressarticle'])
            )
        )

    critic_group = Group.objects.filter(name='CRITIC').first()
    if critic_group:
        critic_group.permissions.set(
            list(view_permissions) + list(
                Permission.objects.filter(codename__in=['add_pressarticle', 'change_pressarticle', 'delete_pressarticle'])
            )
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0017_pressarticle_photo_url'),
    ]

    operations = [
        migrations.RunPython(resync_all_group_permissions, noop),
    ]
