from django.db import models
from django.contrib.auth.models import User


class UserMeta(models.Model):

    class AffiliateTier(models.TextChoices):
        NONE = "none", "Aucun (non affilié)"
        FREE = "free", "Free"
        STARTER = "starter", "Starter"
        PREMIUM = "premium", "Premium"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    langue = models.CharField(max_length=2)
    affiliate_tier = models.CharField(max_length=10, choices=AffiliateTier, default=AffiliateTier.NONE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = "user_meta"
