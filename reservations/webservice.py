import requests
from django.conf import settings

from .models import Show


class WebserviceSyncError(Exception):
    pass


def sync_shows_from_webservice():
    """
    Met a jour le catalogue de spectacles depuis un web service tiers
    (PID : "mettre a jour la liste des spectacles grace aux nouveautes
    publiees par un Web service tiers").

    L'URL est configuree via settings.THIRD_PARTY_CATALOG_API_URL (vide
    par defaut - aucun fournisseur reel n'est branche pour l'instant).
    Le service distant doit repondre en JSON avec une liste d'objets
    {title, description, poster_url, bookable, price}.
    """
    api_url = getattr(settings, 'THIRD_PARTY_CATALOG_API_URL', '')

    if not api_url:
        raise WebserviceSyncError(
            "Aucun web service configure (settings.THIRD_PARTY_CATALOG_API_URL est vide)."
        )

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        raise WebserviceSyncError(f"Echec de la synchronisation : {error}")

    created, updated = 0, 0

    for item in data:
        if not item.get('title'):
            continue

        show, was_created = Show.objects.update_or_create(
            title=item['title'],
            defaults={
                'description': item.get('description', ''),
                'poster_url': item.get('poster_url', ''),
                'bookable': item.get('bookable', False),
                'price': item.get('price', 0),
            },
        )

        if was_created:
            created += 1
        else:
            updated += 1

    return created, updated
