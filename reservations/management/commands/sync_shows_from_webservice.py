from django.core.management.base import BaseCommand, CommandError

from reservations.webservice import sync_shows_from_webservice, WebserviceSyncError


class Command(BaseCommand):
    help = "Met a jour le catalogue de spectacles depuis le web service tiers configure (settings.THIRD_PARTY_CATALOG_API_URL)."

    def handle(self, *args, **options):
        try:
            created, updated = sync_shows_from_webservice()
        except WebserviceSyncError as error:
            raise CommandError(str(error))

        self.stdout.write(self.style.SUCCESS(
            f"Synchronisation terminee : {created} spectacle(s) cree(s), {updated} mis a jour."
        ))
