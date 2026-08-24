from django.db import models

class Location(models.Model):
    slug = models.CharField(max_length=60, null=True, blank=True, unique=True)
    designation = models.CharField(max_length=60, null=True, blank=True, unique=True)
    address = models.CharField(max_length=60, null=False, blank=True)
    website = models.CharField(max_length=255, null=False, blank=True)
    phone = models.CharField(max_length=30, null=False, blank=True)

    def __str__(self):
        return self.designation

    class Meta:
        db_table = "locations"