def role_flags(request):
    """
    Drapeaux de role disponibles dans tous les templates (utilises par
    layouts/base.html pour la visibilite des liens du menu "Mon compte").
    """
    if not request.user.is_authenticated:
        return {'user_is_admin': False, 'user_is_producer': False}

    user = request.user

    return {
        'user_is_admin': user.is_superuser or user.groups.filter(name='ADMIN').exists(),
        'user_is_producer': user.groups.filter(name='PRODUCER').exists(),
    }
