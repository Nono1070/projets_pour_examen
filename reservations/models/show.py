from django.db import models

from .location import Location


class Show(models.Model):
    slug = models.CharField(max_length=60, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(null=False, blank=True)
    poster_url = models.CharField(max_length=255, null=False, blank=True)
    duration = models.PositiveSmallIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='shows')
    bookable = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"
