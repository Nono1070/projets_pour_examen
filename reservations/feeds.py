from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone

from .models import Representation


class UpcomingRepresentationsFeed(Feed):
    title = "Projet Réservations - Prochaines représentations"
    description = "Liste des prochaines représentations de spectacles."

    def link(self):
        return reverse('reservations:index')

    def items(self):
        return Representation.objects.filter(schedule__gte=timezone.now()).order_by('schedule')[:20]

    def item_title(self, item):
        return f"{item.show.title} - {item.schedule:%d/%m/%Y %H:%M}"

    def item_description(self, item):
        location = item.location.designation if item.location else (item.show.location.designation if item.show.location else "")
        return f"{item.show.description} (lieu : {location})"

    def item_link(self, item):
        return reverse('reservations:show_representation', args=[item.id])

    def item_pubdate(self, item):
        return item.schedule
