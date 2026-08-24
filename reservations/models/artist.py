from django.db import models
from .type import *


class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    types = models.ManyToManyField(Type, related_name='artists', db_table='artist_type')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        db_table = "artists"