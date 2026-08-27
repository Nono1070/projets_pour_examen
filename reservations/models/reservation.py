from django.db import models
from django.contrib.auth.models import User

from .representation import Representation


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, related_name='reservations')
    representation = models.ForeignKey(Representation, on_delete=models.RESTRICT, null=False, related_name='reservations')
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.representation} x{self.quantity}"

    class Meta:
        db_table = "reservations"
