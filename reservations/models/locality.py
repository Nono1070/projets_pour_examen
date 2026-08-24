from django.db import models

class Locality(models.Model):
    locality = models.CharField(max_length=60, null=True, blank=True, unique=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True, unique=True)

    def __str__(self):
        return self.locality

    class Meta:
        db_table = "localities"