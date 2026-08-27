from django.db import models
from django.contrib.auth.models import User

from .show import Show


class PressArticle(models.Model):
    critic = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, related_name='press_articles')
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, null=False, related_name='press_articles')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.show.title})"

    class Meta:
        db_table = "press_articles"
