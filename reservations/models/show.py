from django.db import models

class Show(models.Model):
    slug = models.CharField(max_length=60, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField( null=False, blank=True)
    poster_url = models.CharField(max_length=255, null=False, blank=True)
    bookable = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"