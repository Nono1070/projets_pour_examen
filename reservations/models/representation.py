from django.db import models

from .show import Show
from .location import Location


class Representation(models.Model):
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, null=False, related_name='representations')
    schedule = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True, blank=True, related_name='representations')

    def __str__(self):
        return f"{self.show.title} @ {self.schedule}"

    class Meta:
        db_table = "representations"
