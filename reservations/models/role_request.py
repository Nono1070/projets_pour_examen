from django.db import models
from django.contrib.auth.models import User


class RoleRequest(models.Model):

    class Role(models.TextChoices):
        CRITIC = "CRITIC", "Critique de presse"
        PRODUCER = "PRODUCER", "Producteur"

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        APPROVED = "approved", "Approuvée"
        REJECTED = "rejected", "Refusée"

    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='role_requests')
    role = models.CharField(max_length=10, choices=Role)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_role_requests')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} ({self.get_status_display()})"

    class Meta:
        db_table = "role_requests"
